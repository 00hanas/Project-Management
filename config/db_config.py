import mysql.connector

def getConnection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="juhanara20040906",
        database="project_management"
    )
