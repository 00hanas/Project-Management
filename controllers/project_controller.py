import pymysql.cursors #########################################3
from config.db_config import getConnection

# Create
def addProject(project: dict) -> None:
    conn = getConnection()
    cursor = conn.cursor()
    
    sql = "INSERT INTO project (projectID, projectName, shortDescrip, startDate, endDate) VALUES (%s, %s, %s, %s, %s)"
    
    cursor.execute(sql, (
        project["projectID"],
        project["projectName"],
        project["shortDescrip"],
        project["startDate"],
        project["endDate"]
    ))
    
    conn.commit()
    cursor.close()
    conn.close()

# Update
def updateProject(originalID: str, updatedProject: dict) -> None:
    conn = getConnection()
    cursor = conn.cursor()
    
    sql = "UPDATE project SET projectID = %s, projectName = %s, shortDescrip = %s, startDate = %s, endDate = %s WHERE projectID = %s"
    
    values = (
        updatedProject["projectID"],
        updatedProject["projectName"],
        updatedProject["shortDescrip"],
        updatedProject["startDate"],
        updatedProject["endDate"],
        originalID
    )
    
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()

# Delete
def deleteProject(projectID: str) -> None:
    conn = getConnection()
    cursor = conn.cursor()
    
    sql = "DELETE FROM project WHERE projectID = %s"
    
    cursor.execute(sql, (projectID,))
    conn.commit()
    cursor.close()
    conn.close()

# List
def getAllProjects() -> list[tuple]:
    conn = getConnection()
    cursor = conn.cursor()
    
    sql = "SELECT * FROM project"
    
    cursor.execute(sql)
    projects = cursor.fetchall()
    cursor.close()
    conn.close()
    return projects

# Get by ID
def getProjectByID(projectID: str) -> dict | None:
    conn = getConnection()
    cursor = conn.cursor(pymysql.cursors.DictCursor) #########################################################
    
    sql = "SELECT * FROM project WHERE projectID = %s"
    
    cursor.execute(sql, (projectID,))
    project = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if project:
        return {
            "projectID": project["projectID"],
            "projectName": project["projectName"],
            "shortDescrip": project["shortDescrip"],
            "startDate": project["startDate"],
            "endDate": project["endDate"]
        }
        
    return None

def projectExists(projectID: str) -> bool:
    conn = getConnection()
    cursor = conn.cursor()
    
    sql = "SELECT 1 FROM project WHERE projectID = %s"
    
    cursor.execute(sql, (projectID,))
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    
    return exists

def searchProjects(keyword: str) -> list[dict]:
    conn = getConnection()
    cursor = conn.cursor(pymysql.cursors.DictCursor) #########################################################
    
    sql = "SELECT * FROM project WHERE projectName LIKE %s OR shortDescrip LIKE %s"
    
    like = f"%{keyword}%"
    cursor.execute(sql, (like, like))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return results

def assignMemberToProject(projectID: str, memberID: str) -> None:
    conn = getConnection()
    cursor = conn.cursor()
    
    sql = "INSERT INTO projectMember (projectID, memberID) VALUES (%s, %s)"
    
    cursor.execute(sql, (projectID, memberID))
    conn.commit()
    cursor.close()
    conn.close()

def removeMemberFromProject(projectID: str, memberID: str) -> None:
    conn = getConnection()
    cursor = conn.cursor()
    
    sql = "DELETE FROM projectMember WHERE projectID = %s AND memberID = %s"
    
    cursor.execute(sql, (projectID, memberID))
    conn.commit()
    cursor.close()
    conn.close()

def getMembersForProject(projectID: str) -> list[dict]:
    conn = getConnection()
    cursor = conn.cursor(pymysql.cursors.DictCursor) #########################################################
    
    sql = """
        SELECT m.* FROM members m
        JOIN projectMember pm ON m.memberID = pm.memberID
        WHERE pm.projectID = %s
    """
    
    cursor.execute(sql, (projectID,))
    members = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return members

def getProjectsForMember(memberID: str) -> list[dict]:
    conn = getConnection()
    cursor = conn.cursor(pymysql.cursors.DictCursor) #########################################################
    
    sql = """
        SELECT p.* FROM project p
        JOIN projectMember pm ON p.projectID = pm.projectID
        WHERE pm.memberID = %s
    """
    
    cursor.execute(sql, (memberID,))
    projects = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return projects
