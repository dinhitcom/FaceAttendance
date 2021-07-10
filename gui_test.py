import DatabaseUtils
from Utils import *
import cv2
from tkinter import *
from Utils import listAllFolderName, checkFileExist
import os
import face_recognition
from PIL import ImageTk, Image, ImageFont, ImageDraw
from datetime import datetime
import DataEncode
# import Face_Capture

# message = ''
user = {}
user = DatabaseUtils.getUserByEmail('nguyenvana@gmail.com')
isLogged = False
path = 'Image'
numberOfSample = 50
sampleNum = 0
isCapture = False
folderPath = ''
id = ''

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
        if (hashPasswordAndCompare(password, user.Password)):
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
    todayClassList = DatabaseUtils.getAllTodayClassByTeacherId(user.TeacherID)
    def populateTodayClassList():
        for i, todayClass in enumerate(todayClassList):
            todayClassListbox.insert(i, todayClass.ClassName)

    def openFaceCapture():
        faceCaptureWindow = Toplevel()
        faceCaptureWindow.wm_title("Face Capture")
        faceCaptureWindow.config(background="#FFFFFF")
        faceCaptureWindow.geometry('600x600')
        imageFrame = Frame(faceCaptureWindow, width=600, height=500)
        imageFrame.grid(row=0, column=0, padx=10, pady=2)

        lmain = Label(imageFrame)
        lmain.grid(row=0, column=0)
        cap = cv2.VideoCapture(0)

        def show_frame():
            global numberOfSample
            global sampleNum
            global folderPath
            global id
            success, frame = cap.read()
            # frame = cv2.flip(frame, 1)
            saveImg = frame
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if (isCapture and sampleNum < 50):
                faceLocations = face_recognition.face_locations(cv2image)
                if (faceLocations):
                    for faceLocation in faceLocations:
                        y1, x2, y2, x1 = faceLocation
                        cv2.rectangle(frame, (x1 - 5, y1 - 5), (x2 + 5, y2 + 5), (0, 255, 0), 2)
                        if len(faceLocations) > 1:
                            cv2.putText(frame, "Only one face allowed", (10, 25), cv2.FONT_HERSHEY_PLAIN, 2,
                                        (0, 0, 255), 2)
                        else:
                            cv2.putText(frame, f"Captured {sampleNum + 1}/{numberOfSample}", (10, 25),
                                        cv2.FONT_HERSHEY_PLAIN,
                                        2,
                                        (255, 0, 0), 2)
                            timestamp = datetime.today().strftime('%Y%m%d%H%M%S')
                            if cv2.imwrite(folderPath + "/IMG" + id + timestamp + str(sampleNum) + ".jpg", cv2image):
                                sampleNum += 1
                            # print('Captured ' + str(sampleNum))
                            # sampleNum += 1
                else:
                    cv2.putText(frame, "No face found", (10, 25), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            outputImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(outputImage)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(1, show_frame)

        def capture_frame():
            global folderPath
            global isCapture
            global sampleNum
            global id
            id = studentIdText.get()
            if (id):
                folderList = listAllFolderName(path)
                folderPath = os.path.join(path, id)
                if not checkFileExist(folderList, id):
                    os.mkdir(folderPath)
                sampleNum = 0
                isCapture = True
                studentIdEntry.delete(0, END)

        controlFrame = Frame(faceCaptureWindow, width=600, height=100)
        controlFrame.grid(row=1, column=0, padx=10, pady=2)
        studentIdLabel = Label(controlFrame, text='Student ID:', font=('bold', 13), pady=5, padx=5)
        studentIdLabel.grid(row=0, column=0, sticky=W)
        studentIdText = StringVar()
        studentIdEntry = Entry(controlFrame, textvariable=studentIdText, width=15, )
        studentIdEntry.grid(row=0, column=1)
        captureButton = Button(controlFrame, text='Capture', command=capture_frame)
        captureButton.grid(row=0, column=2, padx=5)

        show_frame()


    def encodeAndSaveData():
        statusLabel = Label(mainFrame, text='Loading', font=('bold', 13), pady=10).grid(row=12, column=0)
        DataEncode.EncodeAllImage()
        statusLabel = Label(mainFrame, text='Complete', font=('bold', 13), pady=10).grid(row=12, column=0)

    app = Toplevel()
    app.title("Student Attendance")
    app.geometry('800x500')
    mainFrame = Frame(app)
    # mainFrame.pack()
    mainFrame.grid(row=0, column=0)
    todayClassListLabel = Label(mainFrame, text='Danh sách các lớp hôm nay', font=('bold', 13), pady=10)
    todayClassListLabel.grid(row=0, column=0, sticky=E)

    todayClassListbox = Listbox(mainFrame, height=10, width=72, border=0, selectmode='single', font=('bold', 13))
    todayClassListbox.grid(row=1, column=0, columnspan=8, rowspan=10, padx=20)
    populateTodayClassList()

    attendanceButton = Button(mainFrame, text='Điểm danh', width=12, command=None)
    attendanceButton.grid(row=1, column=10)

    captureButton = Button(mainFrame, text='Chụp ảnh', width=12, command=openFaceCapture)
    captureButton.grid(row=2, column=10)

    encodeButton = Button(mainFrame, text='Encode & Save', width=12, command=encodeAndSaveData)
    encodeButton.grid(row=3, column=10)

# def buildCaptureWindow

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