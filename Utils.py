import os
import cv2
import hashlib
from datetime import datetime

def listAllFolderName(path):
    filenames = os.listdir(path)
    foldernames = []
    for filename in filenames:
        if os.path.isdir(os.path.join(path, filename)):
            foldernames.append(filename)
    return foldernames


def checkFileExist(fileList, name):
    for filename in fileList:
        if name == filename:
            return True
    return False


def loadImagesFromFolder(folderPath):
    images = []
    for filename in os.listdir(folderPath):
        img = cv2.imread(os.path.join(folderPath, filename))
        if img is not None:
            images.append(img)
    return images


def loadAndResizeImagesFromFolder(folderPath, scale):
    images = []
    for filename in os.listdir(folderPath):
        img = cv2.imread(os.path.join(folderPath, filename))
        if img is not None:
            resizedImg = cv2.resize(img, (0, 0), None, 1 / scale, 1 / scale)
            images.append(resizedImg)
    return images


def hashPassword(plainPassword):
    hashPassword = hashlib.md5(plainPassword.encode())
    return hashPassword.hexdigest()


def hashPasswordAndCompare(plainPassword, comparePassword):
    hashedPassword = hashPassword(plainPassword)
    return hashedPassword == comparePassword

def findCurrentDayOfWeek():
    return datetime.today().weekday()

