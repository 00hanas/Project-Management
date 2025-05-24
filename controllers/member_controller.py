from config.db_config import getConnection

#Create
def addMember(member:tuple) -> None:
    conn = getConnection()
    cursor = conn.cursor()

    sql = "INSERT INTO members (memberID, fullname, email) VALUES (%s, %s, %s)"

    cursor.execute(sql, member)
    conn.commit()
    cursor.close()
    conn.close()

#Update
def updateMember(originalID: str, updatedMember: dict) -> None:
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
def deleteMember(memberID: str) -> None:
    conn = getConnection()
    cursor = conn.cursor()

    sql = "DELETE FROM members WHERE memberID = %s"
    cursor.execute(sql, (memberID,))
    conn.commit()
    cursor.close()
    conn.close()

#List
def getAllMembers() -> list[tuple]:
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
            "memberID": member["memberID"],
            "fullname": member["fullname"],
            "email": member["email"]
        }
    return None

def memberExists(memberID: str) -> bool:
    conn = getConnection()
    cursor = conn.cursor()
    
    sql = "SELECT 1 FROM members WHERE memberID = %s"
    
    cursor.execute(sql, (memberID,))
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    
    return exists

def searchMembers(keyword: str) -> list[dict]:
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)
    
    sql = """
        SELECT * FROM members
        WHERE memberID LIKE %s OR fullname LIKE %s OR email LIKE %s
    """
    
    like = f"%{keyword}%"
    
    cursor.execute(sql, (like, like, like))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return results