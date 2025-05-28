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

def assignTasktoMember(member:tuple) -> None:
    conn = getConnection()
    cursor = conn.cursor()

    sql = "INSERT INTO taskMember (taskID, memberID, dateAssigned) VALUES (%s, %s, %s)"

    cursor.execute(sql, member)
    conn.commit()
    cursor.close()
    conn.close()

def assignProjecttoMember(member:tuple) -> None:
    conn = getConnection()
    cursor = conn.cursor()

    sql = "INSERT INTO projectMember (projectID, memberID) VALUES (%s, %s)"

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
        updatedMember[0],
        updatedMember[1],
        updatedMember[2],
        originalID
    )
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()

#Delete
def deleteMemberbyID(memberID: str) -> None:
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
    
    sql = """
    SELECT m.memberID, m.fullname, m.email, 
    COUNT(DISTINCT COALESCE(pm.projectID, tp.projectID)) AS projectCount, 
    COUNT(DISTINCT tm.taskID) AS taskCount 
    FROM members m LEFT JOIN projectMember pm ON m.memberID = pm.memberID 
    LEFT JOIN taskMember tm ON m.memberID = tm.memberID LEFT JOIN task t ON tm.taskID = t.taskID 
    LEFT JOIN project tp ON t.projectID = tp.projectID GROUP BY m.memberID, m.fullname, m.email
    """
    cursor.execute(sql)
    members = cursor.fetchall()
    cursor.close()
    conn.close()
    return members


#Function to load existing data into the edit form
def getMemberByID(memberID: str) -> dict | None:
    conn = getConnection()
    cursor = conn.cursor(dictionary=True) #########################################################
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

def searchMembers(keyword: str, search_by: str) -> list[str]:
    conn = getConnection()
    cursor = conn.cursor()

    keyword_like = f"%{keyword}%"

    sql_base = """
        SELECT DISTINCT m.memberID
        FROM members m
        LEFT JOIN projectMember pm ON m.memberID = pm.memberID
        LEFT JOIN project p ON pm.projectID = p.projectID
        LEFT JOIN taskMember tm ON m.memberID = tm.memberID
        LEFT JOIN task t ON tm.taskID = t.taskID
    """

    if search_by == "Member ID":
        sql = sql_base + " WHERE m.memberID LIKE %s"
        cursor.execute(sql, (keyword_like,))
    elif search_by == "Name":
        sql = sql_base + " WHERE m.fullname LIKE %s"
        cursor.execute(sql, (keyword_like,))
    elif search_by == "Email":
        sql = sql_base + " WHERE m.email LIKE %s"
        cursor.execute(sql, (keyword_like,))
    elif search_by == "Project":
        sql = sql_base + " WHERE p.projectName LIKE %s"
        cursor.execute(sql, (keyword_like,))
    elif search_by == "Task":
        sql = sql_base + " WHERE t.taskName LIKE %s"
        cursor.execute(sql, (keyword_like,))
    else:
        sql = sql_base + """
            WHERE m.memberID LIKE %s OR m.fullname LIKE %s OR m.email LIKE %s
               OR p.projectName LIKE %s OR t.taskName LIKE %s
        """
        cursor.execute(sql, (keyword_like, keyword_like, keyword_like, keyword_like, keyword_like))

    member_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return member_ids #returns only member IDs

#inner table sa expanded row
def getProjectsTasksandDateByMemberID(memberID: str) -> dict:
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)
    
    sql = """
        SELECT
    p.projectID, 
    p.projectName,
    t.taskName,
    date_format(tm.dateAssigned, '%M %e, %Y, %l:%i%p') AS formattedDate
FROM 
    project p
INNER JOIN 
    task t ON p.projectID = t.projectID
INNER JOIN 
    taskMember tm ON t.taskID = tm.taskID
WHERE 
    tm.memberID = %s;
    """
    cursor.execute(sql, (memberID,))
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return tasks

def getProjectsByMemberID(memberID: str) -> list[dict]:
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)
    
    sql = """
        SELECT DISTINCT p.projectID, p.projectName
        FROM project p
        LEFT JOIN projectMember pm ON p.projectID = pm.projectID
        WHERE pm.memberID = %s;
    """
    cursor.execute(sql, (memberID,))
    projects = cursor.fetchall()
    cursor.close()
    conn.close()
    return projects

def getAllMembersForSearch(memberID) -> list[tuple]:
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)
    
    sql = """
    SELECT 
        m.memberID, 
        m.fullname, 
        m.email, 
        COUNT(DISTINCT COALESCE(pm.projectID, tp.projectID)) AS projectCount, 
        COUNT(DISTINCT tm.taskID) AS taskCount 
    FROM members m 
    LEFT JOIN projectMember pm ON m.memberID = pm.memberID 
    LEFT JOIN taskMember tm ON m.memberID = tm.memberID 
    LEFT JOIN task t ON tm.taskID = t.taskID 
    LEFT JOIN project tp ON t.projectID = tp.projectID 
    WHERE m.memberID = %s
    GROUP BY m.memberID, m.fullname, m.email
    """

    cursor.execute(sql, (memberID,))
    members = cursor.fetchone()
    cursor.close()
    conn.close()

    return members

def getProjectIDbyTaskID(taskID: str) -> str | None:
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)
    
    sql = "SELECT projectID FROM task WHERE taskID = %s"
    cursor.execute(sql, (taskID,))
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return result['projectID'] if result else None

def getProjectIDbyMemberID(memberID: str) -> list[str]:
    conn = getConnection()
    cursor = conn.cursor()
    
    sql = "SELECT projectID FROM projectMember WHERE memberID = %s"
    cursor.execute(sql, (memberID,))
    project_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return project_ids

def getTaskIDbyMemberID(memberID: str) -> list[str]:
    conn = getConnection()
    cursor = conn.cursor()
    
    sql = "SELECT taskID FROM taskMember WHERE memberID = %s"
    cursor.execute(sql, (memberID,))
    task_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return task_ids

def clearProjectMember(memberID: str) -> None:
    conn = getConnection()
    cursor = conn.cursor()

    sql = "DELETE FROM projectMember WHERE memberID = %s"
    cursor.execute(sql, (memberID,))
    conn.commit()
    
    cursor.close()
    conn.close()

def clearTaskMember(memberID: str) -> None:
    conn = getConnection()
    cursor = conn.cursor()

    sql = "DELETE FROM taskMember WHERE memberID = %s"
    cursor.execute(sql, (memberID,))
    conn.commit()
    
    cursor.close()
    conn.close()