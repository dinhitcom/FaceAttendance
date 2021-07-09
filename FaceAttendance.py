import cv2
import numpy as np
import face_recognition
import os
import pickle
from PIL import Image, ImageDraw, ImageFont
from constant import RESIZE_SCALE
import DatabaseUtils
from datetime import datetime

FONT_PATH = './arial.ttf'
font = ImageFont.truetype(FONT_PATH, 32)
def attendance(name):
    with open('attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            datetimeString = now.strftime('%H:%M:%S')
            # f.writelines(f'\n{name}, {datetimeString}')

facesData = DatabaseUtils.getAllFaceData()
# print(facesData[1].StudentID)
# print(pickle.loads(facesData[1].EncodedImage))


video_capture = cv2.VideoCapture(0)

while True:
    success, img = video_capture.read()
    resizedImg = cv2.resize(img, (0, 0), None, 1 / RESIZE_SCALE, 1 / RESIZE_SCALE)
    resizedImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    facesCurrentLocation = face_recognition.face_locations(resizedImg)
    encodedCurrentFaces = face_recognition.face_encodings(resizedImg, facesCurrentLocation)
    for currentFace, location in zip(encodedCurrentFaces, facesCurrentLocation):
        minDistance = 0
        id = ""
        name = "Unknown"
        # knownFace = pickle.loads(facesData[0].EncodedImage)
        # test = face_recognition.compare_faces([knownFace], encodedCurrentFaces[0])
        # print(test)
        for i, face in enumerate(facesData):
            faceEncodedData = pickle.loads(face.EncodedImage)
            if face_recognition.compare_faces([faceEncodedData],currentFace):
                faceDistance = face_recognition.face_distance([faceEncodedData], currentFace);
                if i == 0:
                    minDistance = faceDistance
                    id = face.StudentID
                elif faceDistance < minDistance:
                    minDistance = faceDistance
                    id = face.StudentID
        y1, x2, y2, x1 = location
        cv2.rectangle(img, (x1 - 5, y1 - 5), (x2 + 5, y2 + 5), (0, 255, 0), 2)
        if id != "" and minDistance < 0.5:
            studentData = DatabaseUtils.getStudentNameById(id)
            # cv2.rectangle(img, (x1, y2-35), (x2, y2), (0,255,0), cv2.FILLED)

            name = studentData.FullName +" - "+id
            attendance(studentData.FullName)
        imagePIL = Image.fromarray(img)
        draw = ImageDraw.Draw(imagePIL)
        draw.text((x1, y2 + 25), name, font = font, fill=(255, 255, 255, 0), )
        img = np.array(imagePIL)
    cv2.imshow("Cam", img)
    if cv2.waitKey(1) == ord('q'):
        break;
video_capture.release()
cv2.destroyAllWindows()