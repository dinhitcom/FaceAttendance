import pyodbc
import pickle
from constant import SERVER, DATABASE, PORT, USERNAME, PASSWORD
from Utils import findCurrentDayOfWeek
# print(SERVER, DATABASE, USERNAME, PASSWORD)
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+SERVER+';DATABASE='+DATABASE+';Trusted_Connection=yes;')
cursor = cnxn.cursor()
print('connect database success')
def insertFaceData(id, data):
    for img in data:
        pickledData = pickle.dumps(img)
        count = cursor.execute("""
        INSERT INTO StudentImage(StudentID, EncodedImage) 
        VALUES (?,?)""", id, pickledData).rowcount
        cnxn.commit()

def getAllFaceData():
    cursor.execute("SELECT StudentID, EncodedImage FROM StudentImage")
    return cursor.fetchall()

def getStudentNameById(id):
    cursor.execute("SELECT FullName, Class FROM Student WHERE StudentID = '"+id+"'")
    return cursor.fetchone()

def getUserByEmail(email):
    cursor.execute("SELECT * FROM Teacher WHERE Email = '"+email+"'")
    return cursor.fetchone()

def getAllTodayClassByTeacherId(id):
    day = findCurrentDayOfWeek()
    cursor.execute("SELECT ClassID, ClassName FROM Class WHERE TeacherID = '"+str(id)+"' AND ClassTime = "+str(day)+"")
    return cursor.fetchall()

def closeConnection():
    cursor.close()
    cnxn.close()
