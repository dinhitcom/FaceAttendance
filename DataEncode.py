import cv2
import face_recognition
import Utils
import os
from constant import PATH, RESIZE_SCALE
import DatabaseUtils

def encodeImages(images):
    encodedImages = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodedFaces = face_recognition.face_encodings(img, model='large')
            # encodedImg = face_recognition.face_encodings(img)[0]
        if (encodedFaces):
            encodedImages.append(encodedFaces[0])
    return encodedImages

def EncodeAllImage():
    folderList = Utils.listAllFolderName(PATH)
    print(folderList)
    for folder in folderList:
        id = folder
        folderPath = os.path.join(PATH, folder)
        images = Utils.loadAndResizeImagesFromFolder(folderPath, RESIZE_SCALE)
        print(len(images))
        encodedImages = encodeImages(images)
        print(len(encodedImages))
        # DatabaseUtils.insertFaceData(id, encodedImages)


# EncodeAllImage()


