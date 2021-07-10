import numpy as np
import cv2
from tkinter import *
from Utils import listAllFolderName, checkFileExist
import os
import face_recognition
from PIL import ImageTk, Image
from datetime import datetime

def run():
    path = 'Image'
    numberOfSample = 50
    sampleNum = 0
    isCapture = False
    folderPath = ''
    id = ''
    window = Toplevel()
    window.wm_title("Face Capture")
    window.config(background="#FFFFFF")
    window.geometry('600x600')
    imageFrame = Frame(window, width=600, height=500)
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
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if (isCapture and sampleNum < 50):
            faceLocations = face_recognition.face_locations(cv2image)
            if (faceLocations):
                for faceLocation in faceLocations:
                    y1, x2, y2, x1 = faceLocation
                    cv2.rectangle(frame, (x1 - 5, y1 - 5), (x2 + 5, y2 + 5), (0, 255, 0), 2)
                    if len(faceLocations) > 1:
                        cv2.putText(frame, "Only one face allowed", (10, 25), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                    else:
                        cv2.putText(frame, f"Captured {sampleNum + 1}/{numberOfSample}", (10, 25), cv2.FONT_HERSHEY_PLAIN,
                                    2,
                                    (255, 0, 0), 2)
                        timestamp = datetime.today().strftime('%Y%m%d%H%M%S')
                        if cv2.imwrite(folderPath + "/IMG" + id + timestamp + str(sampleNum) + ".jpg", cv2image):
                            sampleNum += 1
                        print('Captured ' + str(sampleNum))
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

    controlFrame = Frame(window, width=600, height=100)
    controlFrame.grid(row=1, column=0, padx=10, pady=2)
    studentIdLabel = Label(controlFrame, text='Student ID:', font=('bold', 13), pady=5, padx=5)
    studentIdLabel.grid(row=0, column=0, sticky=W)
    studentIdText = StringVar()
    studentIdEntry = Entry(controlFrame, textvariable=studentIdText, width=15, )
    studentIdEntry.grid(row=0, column=1)
    captureButton = Button(controlFrame, text='Capture', command=capture_frame)
    captureButton.grid(row=0, column=2, padx=5)


    show_frame()  # Display

# main()# Starts GUI
# run()