'''

DOCUMENTATION

GUI SCRIPT - Maggiethegsd 2024

One of the three fundamental scripts of the project.

Handles all the rendering and management of the windows and widgets and popups to appear on the screen.
Contains various methods to create windows and tables fundamental to the program. Till now screens done-

1. Login Screen
2. Registration Screen
3. Account deletion Screen
4. Institute Homepage Screen
5. Teacher addition Screen
6. Student addition Screen
7. Teacher table screen
8. Student table screen

Some self methods

1. ShowSuccessMessage(arg:message) => Displays a popup message to inform the USER of the success of an action

2. ShowErrorMesssage(arg:message) => Displays a popup message to inform the USER of the failure of an action

3. RenderTable(arg: root, columnsAndTitles, data) => Creates and displays a table in given root window, with given columns 
as identification and titles as the heading names. Data argument is for the actual data to be inserted in columns. Data is 
contained in a nested list with each element being a list of data itself.

4. RenderNewWindow(arg: windowTitle, width, height) => Creates a new tkinter window with given title, width and height. By default
set to non resizable. FUTURE PLAN: ADD BACKGROUND IMAGE ARGUMENT.

'''

import tkinter as tk
from tkinter import ttk
from tkinter import CENTER, messagebox
from tkinter.font import Font

from turtle import heading
from PIL import Image, ImageTk
from datetime import date

import Backend
from Backend import Account as Account, CheckFieldsBlank

imgPath1 = r'imminentthreat.jpg'
img1 = None

imgPath2 = r'theoryofmind.jpg'
img2 = None

imgPath3 = r'overflow.jpeg'
img3 = None

imgPath4 = r'black ice.jpeg'
img4 = None

imgPath5 = r'inmotion.jpeg'
img4 = None

headingFont = None
lightFont = None
lighterFont = None

def ShowSuccessMessage(msg):
    messagebox.showinfo(title='Success!', message=msg)
    
def ShowErrorMessage(msg):
    messagebox.showwarning(title='Error!', message=msg)

def RenderTable(root, columnsAndTitles, data):
    table = ttk.Treeview(root, columns=tuple(columnsAndTitles.keys()), show='headings', selectmode='browse')
    
    try:
        for column in columnsAndTitles:
            table.heading(column, text=columnsAndTitles[column])
    
        for i in range(len(data)):
            vals = []
            for x in range(len(data[i])):
                vals.append(data[i][x])
            table.insert(parent='', index=i, values=tuple(vals))
            
    except:
        print('Error in rendering table')
        
    else:
        table.pack()
    
    return table

def RenderNewWindow(windowTitle, width, height):
    window = tk.Toplevel()
    window.title(windowTitle)
    window.resizable(False, False)
    window.geometry(f'{width}x{height}')
    
    return window

def RenderLoginScreen():
    root = tk.Tk()
    
    global headingFont, lighterFont, lightFont
    
    #setup fonts
    headingFont = Font(family='OCR A Extended', size='20', weight='bold')
    lightFont = Font(family='OCR A Extended', size='14', weight='normal')
    lighterFont = Font(family='OCR A Extended', size='12', weight='normal')

    root.title('Database Management')
    root.geometry('500x500')
    root.resizable(False, False)
    root.attributes('-alpha', .75)
    
    img1 = ImageTk.PhotoImage(Image.open(imgPath1))

    #windows manager attributes
    transparentColor = '#FE93F2'
    root.wm_attributes('-transparentcolor', transparentColor)

    bgLbl = tk.Label(root, image=img1)
    bgLbl.img = img1
    bgLbl.place(relx=0.5, rely=0.5, anchor='center')

    label1 = tk.Label(root, text='LOGIN', font=headingFont, anchor=tk.CENTER)
    label1.place(x=180, y=75)

    frame = tk.Frame(root, height=400, width=400, background='white')
    frame.place(x=50, y=125)

    bgLblFrame = tk.Label(frame, image=img1)
    bgLblFrame.img = img1
    bgLblFrame.place(relx=0.5, rely=0.5, anchor='center')

    usernameLabel = tk.Label(frame, text='USERNAME: ', background='white', font=lightFont)
    usernameLabel.place(x=40, y=40)

    usernameEntry = tk.Entry(frame, width=18, font=lighterFont, highlightthickness=3)
    usernameEntry.place(x=165, y=43)

    passwordLabel = tk.Label(frame, text='PASSWORD: ', background='white', font=lightFont)
    passwordLabel.place(x=40, y=85)

    passwordEntry = tk.Entry(frame, show='*', width=18, font=lighterFont, highlightthickness=3)
    passwordEntry.place(x=165, y=87)
    
    def TryLogin():
        uname = usernameEntry.get()
        pword = passwordEntry.get()
        
        if (CheckFieldsBlank([uname, pword])):
            ShowErrorMessage("Please enter appropriate entry!")
            return
        
        if (Backend.CheckAccountExists(uname, pword)):
            ShowSuccessMessage('Log in successful.')
            root.withdraw()
            RenderHomepage(uname)
        else:
            ShowErrorMessage('No such credentials found!')

    loginButton = tk.Button(frame, text='Login' ,width=14, font=lighterFont, command=TryLogin)
    loginButton.place(x=110, y=160)

    registerButton = tk.Button(frame, text='Register' ,width=14, font=lighterFont, command=RenderRegistrationScreen)
    registerButton.place(x=110, y=200)
    
    removeAnAccButton = tk.Button(frame, text='Remove an account' ,width=20, font=lighterFont, command=RenderRemoveAccountScreen)
    removeAnAccButton.place(x=80, y=280)

    root.mainloop()

def RenderShowStudentsPage(username):
    #get student ids to plot in a table
    students = Backend.GetStudents(username)
    
    if len(students) == 0:
        messagebox.showinfo(message="No students added! Please add students first.")
        return;

    showStudentPage = RenderNewWindow('Students', 800, 600)
    
    account = Backend.GetAccountInfo(username)
    
    #create main table
    columnsAndTitles={'std_id':'STD ID', 'std_name':'NAME', 'mother_name':'MOTHERS NAME', 'father_name':'FATHER NAME', 'doj':'DATE OF JOINING'}
    table = RenderTable(showStudentPage, columnsAndTitles, students)
    
    def TryRemoveStudent():
        if len(table.selection())==0:
            ShowErrorMessage('Please select a student!')
            return
        
        selection = table.focus()
        #print('info: ')
        std_id=table.item(selection).get('values')[0]
        #print('STD_ID: ', std_id)
        
        try:
            Backend.RemoveStudent(username, std_id)
        except:
            ShowErrorMessage("Could not remove student! Please try again later.")
        else:
            table.delete(selection)
            ShowSuccessMessage("Successfully removed student!")
        
    removeStudentButton = tk.Button(showStudentPage, width=30, text='Remove Selected Student', font=lightFont, command=TryRemoveStudent)
    removeStudentButton.place(x=350, y=450)
    
def RenderShowTeachersPage(username):
    #get teacher ids to plot in a table
    teachers = Backend.GetTeachers(username)
    
    if len(teachers) == 0:
        messagebox.showinfo(message="No teachers added! Please add teachers first.")
        return;

    showTeacherPage = RenderNewWindow('Teachers', 800, 600)
    
    account = Backend.GetAccountInfo(username)
    
    #create main table
    columnsAndTitles={'teacher_id':'TEACHER ID', 'teacher_name':'NAME', 'teacher_subject':'SUBJECT', 'doj':'DATE OF JOINING'}
    table = RenderTable(showTeacherPage, columnsAndTitles, teachers)
    
    def TryRemoveTeacher():
        if len(table.selection())==0:
            ShowErrorMessage("Please select a teacher!")
            return
        
        selection = table.focus()
        teacher_id=table.item(selection).get('values')[0]
        
        try:
            Backend.RemoveTeacher(username, teacher_id)
        except:
            ShowErrorMessage("Could not remove teacher. Please try again!")
        else:
            table.delete(selection)
            ShowSuccessMessage("Successfully removed teacher!")
            
        
    removeTeacherButton = tk.Button(showTeacherPage, width=30, text='Remove Selected Teacher', font=lightFont, command=TryRemoveTeacher)
    removeTeacherButton.place(x=350, y=450)

def RenderAddStudentPage(username):
    addStudentPage = RenderNewWindow('Add a student', 600, 400)
    
    account = Backend.GetAccountInfo(username)
    
    backdrop = tk.Canvas(addStudentPage, width=600, height=50, background='black')
    backdrop.place(x=0, y=0)
    backdrop.create_image(0, 0, image=img1)
    
    label1 = tk.Label(addStudentPage, text='Add a student', font=headingFont, anchor=tk.CENTER)
    label1.place(x=150, y=10)
    
    studentNameLbl = tk.Label(addStudentPage, text='Student name: ', font=lightFont, anchor=tk.CENTER)
    studentNameLbl.place(x=60, y=100)
    
    studentNameEntry = tk.Entry(addStudentPage, font=lightFont)
    studentNameEntry.place(x=210, y=100)
    
    mothersNameLbl = tk.Label(addStudentPage, text='Mothers name: ' , font=lightFont, anchor=tk.CENTER)
    mothersNameLbl.place(x=60, y=150)
    
    mothersNameEntry = tk.Entry(addStudentPage, font=lightFont)
    mothersNameEntry.place(x=210, y=150) 
    
    fathersNameLbl = tk.Label(addStudentPage, text='Fathers name: ' , font=lightFont, anchor=tk.CENTER)
    fathersNameLbl.place(x=60, y=200)
    
    fathersNameEntry = tk.Entry(addStudentPage, font=lightFont)
    fathersNameEntry.place(x=210, y=200)
    
    def TryAddStudent():
        studentName = studentNameEntry.get()
        fathersName = fathersNameEntry.get()
        mothersName = mothersNameEntry.get()
        
        if CheckFieldsBlank([studentName, fathersName, mothersName]):
            ShowErrorMessage('Please enter non blank values!')
            
        else:
            status = Backend.AddStudent(username, studentName, mothersName, fathersName, str(date.today()))
            if (status):
                ShowSuccessMessage('Successfully added student!')
            else:
                ShowErrorMessage('Error Occured!')
                
            
    addStudentBtn = tk.Button(addStudentPage, width = 10, text='Add Student', font=lightFont, command=TryAddStudent)
    addStudentBtn.place(x=240, y=300)
    
def RenderAddTeacherPage(username):
    addTeacherPage = RenderNewWindow('Add a teacher', 600, 400)
    
    account = Backend.GetAccountInfo(username)
    
    backdrop = tk.Canvas(addTeacherPage, width=600, height=50, background='black')
    backdrop.place(x=0, y=0)
    backdrop.create_image(0, 0, image=img1)
    
    label1 = tk.Label(addTeacherPage, text='Add a teacher', font=headingFont, anchor=tk.CENTER)
    label1.place(x=150, y=10)
    
    teacherNameLbl = tk.Label(addTeacherPage, text='Teacher name: ', font=lightFont, anchor=tk.CENTER)
    teacherNameLbl.place(x=60, y=100)
    
    teacherNameEntry = tk.Entry(addTeacherPage, font=lightFont)
    teacherNameEntry.place(x=210, y=100)
    
    teacherSubjectLbl = tk.Label(addTeacherPage, text='Teacher subject: ' , font=lightFont, anchor=tk.CENTER)
    teacherSubjectLbl.place(x=60, y=150)
    
    teacherSubjectEntry = tk.Entry(addTeacherPage, font=lightFont)
    teacherSubjectEntry.place(x=240, y=150) 
    
    def TryAddTeacher():
        teacherName = teacherNameEntry.get()
        teacherSubject = teacherSubjectEntry.get()
        
        if CheckFieldsBlank([teacherName, teacherSubject]):
            ShowErrorMessage('Please enter non blank values!')
            
        else:
            status = Backend.AddTeacher(username, teacherName, teacherSubject, str(date.today()))
            if (status):
                ShowSuccessMessage('Successfully added teacher!')
            else:
                ShowErrorMessage('Error Occured!')
                
            
    addTeacherBtn = tk.Button(addTeacherPage, width = 10, text='Add Student', font=lightFont, command=TryAddTeacher)
    addTeacherBtn.place(x=240, y=300)
    
def RenderHomepage(username):
    homePage = RenderNewWindow('Homepage', 750, 750)
    
    account = Backend.GetAccountInfo(username)
    
    img3 = ImageTk.PhotoImage(Image.open(imgPath3).resize((750,750)))

    #BACKGROUND
    bgLbl = tk.Label(homePage, image=img3)
    bgLbl.img = img3
    bgLbl.place(relx=0.5, rely=0.5, anchor='center')
    
    bgLblFrame = tk.Label(homePage, image=img3)
    bgLblFrame.img = img3
    bgLblFrame.place(relx=0.5, rely=0.5, anchor='center')
    
    backdrop = tk.Canvas(homePage, width=750, height=100, background='white')
    backdrop.place(relx=0.5,rely=0, anchor='n')
    backdrop.create_image(0, 0, image=img1)
    
    instituteNameDisplay = tk.Label(backdrop, text=account.instituteName, font=headingFont, anchor=tk.CENTER)
    instituteNameDisplay.place(relx=0.35, rely=0.25)
    
    instituteCityDisplay = tk.Label(backdrop, text=account.instituteCity, font=lightFont, anchor=tk.CENTER)
    instituteCityDisplay.place(relx=0.45, rely=0.8, anchor='center')
    
    #STUDENT ACTIONS
    studentActions = tk.Frame(homePage, width=300, height=400, background='white')
    studentActions.place(x=50, y=125)
    
    studentActionsLbl = tk.Label(studentActions, text='Student Actions', font=lightFont)
    studentActionsLbl.grid(row=0, column=0, padx=15, pady=10)
    
    showStudentsBtn = tk.Button(studentActions, text='Show students', font=lightFont, command = lambda: RenderShowStudentsPage(username))
    showStudentsBtn.grid(row=1, column = 0, padx=15, pady=5)
    
    addStudentBtn = tk.Button(studentActions, text='Add a student', font=lightFont, command= lambda: RenderAddStudentPage(username))
    addStudentBtn.grid(row=2, column = 0, padx=15, pady=15)
    
    #TEACHER ACTIONS
    teacherActions = tk.Frame(homePage, width=300, height=400, background='white')
    teacherActions.place(x=300, y=125)
    
    teacherActionsLbl = tk.Label(teacherActions, text='Teacher Actions', font=lightFont)
    teacherActionsLbl.grid(row=0, column=0, padx=15, pady=10)
    
    showTeachersBtn = tk.Button(teacherActions, text='Show teachers', font=lightFont, command = lambda: RenderShowTeachersPage(username))
    showTeachersBtn.grid(row=1, column = 0, padx=15, pady=5)
    
    addTeacherBtn = tk.Button(teacherActions, text='Add a teacher', font=lightFont, command= lambda: RenderAddTeacherPage(username))
    addTeacherBtn.grid(row=2, column = 0, padx=15, pady=15)
    
    teacherActions.columnconfigure(0, weight=1)
    
    homePage.title(account.instituteName)

def RenderRegistrationScreen():
    registrationWindow = RenderNewWindow('Register an account', 550, 500)
    
    #BACKGROUND IMAGE
    img4 = ImageTk.PhotoImage(Image.open(imgPath4).resize((550, 500)))

    bgLbl = tk.Label(registrationWindow, image=img4)
    bgLbl.img = img4
    bgLbl.place(relx=0.5, rely=0.5, anchor='center')
    
    bgLblFrame = tk.Label(registrationWindow, image=img4)
    bgLblFrame.img = img4
    bgLblFrame.place(relx=0.5, rely=0.5, anchor='center')
    
    label1 = tk.Label(registrationWindow, text='REGISTER', font=headingFont, anchor=tk.CENTER)
    label1.place(x=175, y=80)
    
    label2 = tk.Label(registrationWindow, text='Username: ', font=lightFont)
    label2.place(x=100, y=160)
    
    usernameEntry = tk.Entry(registrationWindow, font=lighterFont)
    usernameEntry.place(x=230, y=163)
    
    label3 = tk.Label(registrationWindow, text='Institute Name: ', justify=CENTER, font=lightFont)
    label3.place(x=50, y=200)
    
    instituteNameEntry = tk.Entry(registrationWindow, font=lighterFont)
    instituteNameEntry.place(x=230, y=200)
    
    label4 = tk.Label(registrationWindow, text='Institute City:', justify=CENTER, font=lightFont)
    label4.place(x=60, y=240)
    
    instituteCityEntry = tk.Entry(registrationWindow, font=lighterFont)
    instituteCityEntry.place(x=230, y=240)
    
    label5 = tk.Label(registrationWindow, text='Password:', justify=CENTER, font=lightFont)
    label5.place(x=100, y=280)
    
    passwordEntry = tk.Entry(registrationWindow, font=lighterFont)
    passwordEntry.place(x=230, y=280)
    
    label5 = tk.Label(registrationWindow, text='Please remember this username and password!', justify=CENTER, font=lightFont)
    label5.place(x=35, y=320)
    
    def TryRegister():
        if (CheckFieldsBlank([usernameEntry.get(), instituteNameEntry.get(), instituteCityEntry.get()])):
            ShowErrorMessage('Input cannot be blank!')
            return
        
        registered = Backend.RegisterAccount(usernameEntry.get(), instituteNameEntry.get(), instituteCityEntry.get(), passwordEntry.get())
        if (registered):
            ShowSuccessMessage('Registration successful!')
            registrationWindow.withdraw()
        else:
            ShowErrorMessage('Account with same username exists!')
            
    registerBtn = tk.Button(registrationWindow, text='Register', width=14, font=lightFont, command=TryRegister)
    registerBtn.place(x=150, y=380)
    
def RenderRemoveAccountScreen():
    removalWindow = RenderNewWindow('Remove an account', 550, 400)
    
    img2 = ImageTk.PhotoImage(Image.open(imgPath3).resize((550, 400)))

    bgLbl = tk.Label(removalWindow, image=img2)
    bgLbl.img = img2
    bgLbl.place(relx=0.5, rely=0.5, anchor='center')
    
    bgLblFrame = tk.Label(removalWindow, image=img2)
    bgLblFrame.img = img2
    bgLblFrame.place(relx=0.5, rely=0.5, anchor='center')
    
    label1 = tk.Label(removalWindow, text='REMOVE AN ACCOUNT', font=headingFont, anchor=tk.CENTER)
    label1.place(x=120, y=80)
    
    label2 = tk.Label(removalWindow, text='Username: ', font=lightFont)
    label2.place(x=100, y=160)
    
    usernameEntry = tk.Entry(removalWindow, font=lighterFont)
    usernameEntry.place(x=215, y=163)
    
    label5 = tk.Label(removalWindow, text='Password:', justify=CENTER, font=lightFont)
    label5.place(x=100, y=190)
    
    passwordEntry = tk.Entry(removalWindow, font=lighterFont)
    passwordEntry.place(x=215, y=193)
    
    confirmation1 = tk.IntVar()
    confirmationCheck1 = tk.Checkbutton(removalWindow, text='I understand on deletion of an account, it cannot be recovered', onvalue=1, offvalue=0, variable=confirmation1)
    confirmationCheck1.place(x=100, y=240)
    
    confirmation2 = tk.IntVar()
    confirmationCheck2 = tk.Checkbutton(removalWindow, text='I am not a robot', onvalue=1, offvalue=0, variable=confirmation2)
    confirmationCheck2.place(x=100, y=260)
    
    def TryRemoveAccount():
        if (confirmation1.get() == 0 or confirmation2.get() == 0):
            ShowErrorMessage("Please tick checkboxes for confirmation!")
            return
            
        if (CheckFieldsBlank([usernameEntry.get(), passwordEntry.get()])):
            ShowErrorMessage('Input cannot be blank!')
            return
        
        if (Backend.CheckAccountExists(usernameEntry.get(), passwordEntry.get()) == False):
            ShowErrorMessage('No such account found!')
            return
        
        confirmationMessage = messagebox.askyesno(title='Delete account?', message='Account found. Are you sure you want to delete this account?')
        
        if (confirmationMessage == True):
            deleted = Backend.RemoveAccount(usernameEntry.get(), passwordEntry.get())
            if (deleted):
                ShowSuccessMessage('Account deletion successful!')
                removalWindow.withdraw()
            else:
                ShowErrorMessage('Error in deletion. Please try again.')    
            
    registerBtn = tk.Button(removalWindow, text='Remove account', width=13, font=lightFont, command=TryRemoveAccount)
    registerBtn.place(x=190, y=290)
 
