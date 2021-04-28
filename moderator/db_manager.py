import pyodbc
import os

os.chdir("..")
print(os.getcwd(), os.listdir("datas"))
def get_dbconn(file, password=None):
    pyodbc.pooling = False
    driver = '{Microsoft Access Driver (*.mdb)}'
    dbdsn = f'Driver={driver};Dbq={file};'
    if password:
        dbdsn += f'Pwd={password};'
    return pyodbc.connect(dbdsn)

conn = get_dbconn("C:\Users\Zsuzsa\Documents\GitHub\dcmoderator\datas\mutes.mdb")