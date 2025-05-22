from config.db_config import getConnection

#Create
def addMember(member):
    conn = getConnection()
    cursor = conn.cursor()

    sql = "INSERT INTO members (memberID, fullname, email) VALUES (%s, %s, %s)"

    cursor.execute(sql, member)
    conn.commit()
    cursor.close()
    conn.close()

#Update
def updateMember(originalID, updatedMember):
    conn = getConnection()
    cursor = conn.cursor()

    sql = "UPDATE members SET memberID = %s, fullname = %s, email = %s WHERE memberID = %s"

    values = (
        updatedMember["memberID"],
        updatedMember["fullname"],
        updatedMember["email"],
        originalID
    )
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()

#Delete
def deleteMember(memberID):
    conn = getConnection()
    cursor = conn.cursor()

    sql = "DELETE FROM members WHERE memberID = %s"
    cursor.execute(sql, (memberID,))
    conn.commit()
    cursor.close()
    conn.close()

#List
def getAllMembers():
    conn = getConnection()
    cursor = conn.cursor()
    sql = "SELECT * FROM members"
    cursor.execute(sql)
    members = cursor.fetchall()
    cursor.close()
    conn.close()
    return members


#Function to load existing data into the edit form
def getMemberByID(memberID: str) -> dict | None:
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM members WHERE memberID = %s"
    cursor.execute(sql, (memberID,))
    member = cursor.fetchone()
    cursor.close()
    conn.close()

    if member:
        return {
            "memberID": member[0],
            "fullname": member[1],
            "email": member[2]
        }
    return None

