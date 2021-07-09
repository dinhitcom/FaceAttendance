from tkinter import *
import DatabaseUtils
import Utils

# message = ''
user = {}
user = DatabaseUtils.getUserByEmail('nguyenvana@gmail.com')
isLogged = False
def cancelLogin():
    login.destroy()
    sys.exit

def validateLogin():
    # global message
    global user
    message = ''
    username = usernameText.get()
    password = passwordText.get()
    user = DatabaseUtils.getUserByEmail(username)
    if (user):
        if (Utils.hashPasswordAndCompare(password, user.Password)):
            login.withdraw()
            buildAppWindow()
            return ''
        else:
            message = "Incorrect password!"
    else:
        message = "User not found"
    messageLabel = Label(login, text=message, font=('bold', 13), fg='#ff0000')
    messageLabel.grid(row=2, column=0, columnspan=3)



def buildAppWindow():

    def populateTodayClassList():
        todayClassList = DatabaseUtils.getAllTodayClassByTeacherId(user.TeacherID)
        for i, todayClass in enumerate(todayClassList):
            todayClassListbox.insert(i, todayClass.ClassName)

    app = Toplevel()
    app.title("Student Attendance")
    app.geometry('800x500')
    # mainFrame = Frame(app)
    # mainFrame.pack()
    todayClassListLabel = Label(app, text='Danh sách các lớp hôm nay', font=('bold', 13), pady=10)
    todayClassListLabel.grid(row=0, column=0, sticky=E)

    todayClassListbox = Listbox(app, height=10, width=72, border=0, selectmode='single', font=('bold', 13))
    todayClassListbox.grid(row=1, column=0, columnspan=8, rowspan=10, padx=20)
    populateTodayClassList()

    attendanceButton = Button(app, text='Điểm danh', width=12)
    attendanceButton.grid(row=1, column=10)

    captureButton = Button(app, text='Chụp ảnh', width=12)
    captureButton.grid(row=2, column=10)


login = Tk()
login.title("Login")
login.geometry('350x130')

usernameText = StringVar()
usernameLabel = Label(login, text='Email:', font=('bold', 13), pady=10,)
usernameLabel.grid(row=0, column=0, sticky=W)
usernameEntry = Entry(login, textvariable=usernameText, width=25)
usernameEntry.grid(row=0, column=1, padx=10)

passwordText = StringVar()
passwordLabel = Label(login, text='Password:', font=('bold', 13))
passwordLabel.grid(row=1, column=0, sticky=W, pady=10)
passwordEntry = Entry(login, textvariable=passwordText, show='*', width=25)
passwordEntry.grid(row=1, column=1, padx=10)

loginButton = Button(login, text='Login', command=validateLogin, padx=5, width=8)
loginButton.grid(row=0, column=2, sticky=E)
cancelButton = Button(login, text='Cancel', command=cancelLogin, padx=5, width=8)
cancelButton.grid(row=1, column=2, sticky=E)

buildAppWindow()

login.withdraw()

# app.withdraw()
login.mainloop()

#nguyenvana@gmail.com