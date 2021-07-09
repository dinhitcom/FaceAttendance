from datetime import datetime

import cv2
import face_recognition
import os
import Utils

path = 'Image'
numberOfSample = 50;
video_capture = cv2.VideoCapture(0)
id = input("Nhập id: ")
alreadyExists = False
folderList = Utils.listAllFolderName(path)
folderPath = os.path.join(path, id)

if not Utils.checkFileExist(folderList, id):
    os.mkdir(folderPath)

sampleNum = 0

while True:
    success, img = video_capture.read()
    cvtImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.flip(img, 1)
    saveImg = img
    faceLocations = face_recognition.face_locations(cvtImg)

    if faceLocations:
        for face in faceLocations:
            y1, x2, y2, x1 = face
            cv2.rectangle(img, (x1 - 5, y1 - 5), (x2 + 5, y2 + 5), (0, 255, 0), 2)

        if len(faceLocations) > 1:
            cv2.putText(img, "Only one face allowed", (10, 25), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        else:
            cv2.putText(img, f"Captured {sampleNum + 1}/{numberOfSample}", (10, 25), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            timestamp = datetime.today().strftime('%Y%m%d%H%M%S')
            if cv2.imwrite(folderPath + "/IMG" + id + timestamp + str(sampleNum) + ".jpg", saveImg):
                sampleNum += 1
            print('Captured ' + str(sampleNum))
            # sampleNum += 1
    else:
        cv2.putText(img, "No face found", (10, 25), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

    cv2.imshow("Camera Capture", img)

    if cv2.waitKey(1) == ord('q'):
        break
    elif sampleNum >= numberOfSample:
        break

video_capture.release()
cv2.destroyAllWindows()