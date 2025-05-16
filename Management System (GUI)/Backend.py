'''

DOCUMENTATION 

Backend Script - Maggiethegsd 2024

One of the three fundamental scripts of the project.

Handles all the backend SQL server connection work, which is the heart of the project. 
Contains core methods to create institute accounts, add teachers and students to institutes.

Some self methods

1. CheckFieldsBlank(arg:fields) => Takes input of a list of string and checks whether any string is blank or has whitespace.
Essential function for handling input of tkinter entry fields such as username, password, etc.

2. CleanupString(arg:string) => Takes input of a string and cleans it up by titling it, and removing trailing and leading whitespaces.

3. GetAccountInfo(arg:username) => Returns 'Account' type data by reading local file with given username. Account type data contains everything from
teachers to students to institue username, password, etc.

'''


import atexit
import pickle
from uu import Error
import mysql.connector as connector
import os

class Account:
    def __init__(self, username, instituteName, instituteCity, password):
        self.username = username
        self.instituteName = instituteName 
        self.instituteCity = instituteCity
        self.password = password
        self.students = {}
        self.teachers = {}
        
#self setup - create foundation database for this entire program
preConnection = connector.connect(host='localhost', username='coaching', password='password')
preConnection.cursor().execute('CREATE DATABASE IF NOT EXISTS coachingManagement')

#root connection for carrying out all tasks
connection = connector.connect(host='localhost', username='coaching', password='password', database='coachingManagement')
connection.autocommit = True
atexit.register(connection.close)

#create table of accounts and passwords
#self setup - create accounts table
cursor = connection.cursor(buffered=True)
cursor.execute('CREATE TABLE IF NOT EXISTS ACCOUNTS(username VARCHAR(25), instituteName VARCHAR(25), instituteCity VARCHAR(25), password VARCHAR(25))')

#returns true if any of the fields entered is whitespace
def CheckFieldsBlank(fields):
    empty = False
    
    for field in fields:
       if (str(field).isspace() or len(field)==0):
          empty = True
          break
                
    return empty

#return a nicely formatted string for use 
def CleanupString(string):
    formatted = str(string).strip()
    formatted = string.title()
    
    return formatted
        
def GetAccountInfo(username):
    with open(f'{username}.dat', 'rb') as accountFile:
        return pickle.load(accountFile)
        #return type: Account
    
    
def GetStudents(username):
    #fetch students from server
    cursor.execute(f'SELECT * FROM {username}_students')
    #print(cursor.fetchall())
    
    return cursor.fetchall()
    #returns tuple of lists. Each list contains student info sequentially.

def GetTeachers(username):
    #fetch students from server
    cursor.execute(f'SELECT * FROM {username}_teachers')
    #print(cursor.fetchall())
    
    return cursor.fetchall()
    #returns tuple of lists. Each list contains teacher info sequentially.
    

def AddStudent(instituteUsername, std_name, std_mothersName, std_fathersName, std_doj):
    existing = cursor.execute(f"SELECT COUNT(*) FROM {instituteUsername}_students;")
    existingStudents = cursor.fetchone()[0]
    std_id = existingStudents+1 
    
    try:
        #add to server
        cursor.execute(f"INSERT INTO {instituteUsername}_students VALUES({std_id}, '{std_name}', '{std_mothersName}', '{std_fathersName}', '{std_doj}');")
        
        #add to local file
        GetAccountInfo(instituteUsername).students[std_id] = std_name
        
    except:
        print(f'Could not add student {std_name} to {instituteUsername}_students')
        return False
    
    else:
        return True
    
def RemoveStudent(instituteUsername, std_id):
    try:
        #remove from server
        cursor.execute(f"DELETE FROM {instituteUsername}_students WHERE STD_ID = {std_id};")
        
        #remove from local file
        GetAccountInfo(instituteUsername).students.pop(std_id)
        
    except:
        print(f'Could not remove student of id {std_id} from {instituteUsername}_students')
        return False
    
    else:
        return True
    
def AddTeacher(instituteUsername, teacher_name, teacher_subject, teacher_doj):
    existing = cursor.execute(f"SELECT COUNT(*) FROM {instituteUsername}_teachers;")
    existingTeachers = cursor.fetchone()[0]
    teacher_id = existingTeachers+1 
    
    try:
        #add to server
        cursor.execute(f"INSERT INTO {instituteUsername}_teachers VALUES({teacher_id}, '{teacher_name}', '{teacher_subject}', '{teacher_doj}');")
        
        #add to local file
        GetAccountInfo(instituteUsername).teachers[teacher_id] = teacher_name
    except Exception as e:
        print(f'Could not add teacher {teacher_name} to {instituteUsername}_teachers')
        print(f'ERROR: {e}')
        return False
    
    else:
        return True
    
def RemoveTeacher(instituteUsername, teacher_id):
    try:
        #remove from server
        cursor.execute(f"DELETE FROM {instituteUsername}_teachers WHERE TEACHER_ID = {teacher_id};")
        
        #remove from local file
        GetAccountInfo(instituteUsername).teachers.pop(teacher_id)
        
    except:
        print(f'Could not remove teacher of id {teacher_id} from {instituteUsername}_teacher')
        return False
    
    else:
        return True
    
def RegisterAccount(username, instituteName, instituteCity, password):
    usersWithSame = cursor.execute(f"SELECT USERNAME FROM ACCOUNTS WHERE USERNAME='{username}'")
    
    if len(cursor.fetchall()) > 0:
        return False
    
    try:
        #server side create account
        cursor.execute(f"INSERT INTO ACCOUNTS VALUES('{username}', '{instituteName}', '{instituteCity}', '{password}');")
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {username}_students(STD_ID int primary key, STD_NAME varchar(30), STD_MOTHERSNAME varchar(30), STD_FATHERSNAME varchar(30), STD_DOJ date)")
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {username}_teachers(TEACHER_ID int primary key, TEACHER_NAME varchar(30), TEACHER_SUBJECT varchar(30), TEACHER_DOJ date)")
    
        #locally also create account file
        with open(f'{username}.dat', 'wb+') as instituteFile:
           newAccount = Account(username, instituteName, instituteCity, password)
       
           pickle.dump(newAccount, instituteFile)
    except:
        return False
    else:
        return True

#CAUTION WITH THIS FUNCTION
def RemoveAccount(username, password):
    usersWithSame = cursor.execute(f"SELECT USERNAME FROM ACCOUNTS WHERE USERNAME='{username}' AND PASSWORD='{password}'")
    
    if len(cursor.fetchall()) == 0:
        return False
    
    try:
        #server side remove account
        cursor.execute(f"DELETE FROM ACCOUNTS WHERE USERNAME='{username}' AND PASSWORD='{password}'")
        #note, AND PASSWORD clause was not necessary since two accounts with same username cannot exist
    
        cursor.execute(f"DROP TABLE IF EXISTS {username}_students")
        cursor.execute(f"DROP TABLE IF EXISTS {username}_teachers")
    
        #locally delete file
        if (os.path.exists(f'{username}.dat')):
            os.remove(f'{username}.dat')
            
    except Exception as  e:
        print(e)
        return False
    else:
        return True
    

def CheckAccountExists(username, password):
    global cursor
    users = cursor.execute(f"SELECT USERNAME, PASSWORD FROM ACCOUNTS WHERE username='{username}' AND password='{password}';")
    
    return len(cursor.fetchall()) > 0
        
if (connection.is_connected()):
    print('Successfully connected! ')
    
else:
    print('There was some error in connection')
        

