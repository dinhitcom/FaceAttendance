import pyodbc
import pickle
from constant import SERVER, DATABASE, PORT, USERNAME, PASSWORD
# print(SERVER, DATABASE, USERNAME, PASSWORD)
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+SERVER+';DATABASE='+DATABASE+';Trusted_Connection=yes;')
cursor = cnxn.cursor()
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

def getNameAndClassById(id):
    cursor.execute("SELECT StudentName, Class FROM StudentInformation WHERE StudentID = '"+id+"'")
    return cursor.fetchone()
print('connect database success')
# dinh = getNameAndClassById("18IT269")
# print(dinh)