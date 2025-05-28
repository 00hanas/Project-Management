import pymysql.cursors
import pymysql
from config.db_config import getConnection
from datetime import datetime
import pymysql.cursors #########################################3


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

# Get total tasks for a project
def getTotalTasks(projectID: str) -> int:
    conn = getConnection()
    cursor = conn.cursor()
    
    sql = "SELECT COUNT(*) FROM task WHERE projectID = %s"
    
    cursor.execute(sql, (projectID,))
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total

# Get all completed tasks for a project
def getCompletedTasks(projectID: str) -> int:
    conn = getConnection()
    cursor = conn.cursor()
    
    sql = "SELECT COUNT(*) FROM task WHERE projectID = %s AND currentStatus = 'Completed'"
    
    cursor.execute(sql, (projectID,))
    completed = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return completed

# Get by ID
def getProjectByID(projectID: str) -> dict | None:
    conn = getConnection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
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

def searchProjects(keyword: str, search_by: str) -> list[dict]:
    if not keyword.strip():
        return []
        
    conn = getConnection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if not keyword.strip():
        cursor.execute("SELECT projectID FROM project")
        return cursor.fetchall()
    
    keyword_like = f"%{keyword}%"
    
    # Use parameterized queries to prevent SQL injection
    if search_by == "Project ID":
        sql = "SELECT projectID FROM project WHERE projectID LIKE %s LIMIT 100"
        params = (keyword_like,)
    elif search_by == "Project Name":
        sql = "SELECT projectID FROM project WHERE projectName LIKE %s LIMIT 100"
        params = (keyword_like,)
    elif search_by == "Start Date":
        sql = "SELECT projectID FROM project WHERE DATE_FORMAT(startDate, '%%Y-%%m-%%d') LIKE %s LIMIT 100"
        params = (keyword_like,)
    elif search_by == "End Date":
        sql = "SELECT projectID FROM project WHERE DATE_FORMAT(endDate, '%%Y-%%m-%%d') LIKE %s LIMIT 100"
        params = (keyword_like,)
    else:
        sql = """
            SELECT projectID FROM project 
            WHERE projectID LIKE %s 
               OR projectName LIKE %s 
               OR DATE_FORMAT(startDate, '%%Y-%%m-%%d') LIKE %s
               OR DATE_FORMAT(endDate, '%%Y-%%m-%%d') LIKE %s
            LIMIT 100
        """
        params = (keyword_like,) * 5

    try:
        cursor.execute(sql, params)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def parse_date(date_str):
    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return date_str 

def getAllProjectsForSearch(project_ids: list[str]) -> list[tuple]:
    conn = getConnection()
    cursor = conn.cursor()

    if not project_ids:
        return []

    placeholders = ', '.join(['%s'] * len(project_ids))
    sql = f"SELECT * FROM project WHERE projectID IN ({placeholders})"

    cursor.execute(sql, (project_ids))
    projects = cursor.fetchall()

    cursor.close()
    conn.close()
    return projects

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

# Get members for a specific project
def getMembersForProject(projectID: str) -> list[dict]:
    conn = getConnection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

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

# Get projects for a specific member
def getProjectsForMember(memberID: str) -> list[dict]:
    conn = getConnection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
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

def sortProjects(sort_by: str, ascending: bool = True) -> list[dict]:
    conn = getConnection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    # Map UI sort options to database columns
    sort_mapping = {
        "Name": "projectName",
        "Project ID": "projectID",
        "Start Date": "startDate",
        "End Date": "endDate"
    }
    
    if sort_by not in sort_mapping:
        sort_by = "projectName"  # Default sort
    
    order = "ASC" if ascending else "DESC"
    
    sql = f"SELECT * FROM project ORDER BY {sort_mapping[sort_by]} {order}"
    
    cursor.execute(sql)
    projects = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return projects