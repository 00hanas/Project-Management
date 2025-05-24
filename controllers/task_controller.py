from config.db_config import getConnection

# --- CRUD for Task ---

def addTask(task: dict) -> None:
    conn = getConnection()
    cursor = conn.cursor()
    
    sql = """
        INSERT INTO task (taskID, taskName, shortDescrip, currentStatus, dueDate, dateAccomplished, projectID)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    cursor.execute(sql, (
        task["taskID"],
        task["taskName"],
        task.get("shortDescrip"),
        task["currentStatus"],
        task.get("dueDate"),
        task.get("dateAccomplished"),
        task["projectID"]
    ))
    
    conn.commit()
    cursor.close()
    conn.close()

def updateTask(originalID: str, updatedTask: dict) -> None:
    conn = getConnection()
    cursor = conn.cursor()
    
    sql = """
        UPDATE task
        SET taskID = %s, taskName = %s, shortDescrip = %s, currentStatus = %s, dueDate = %s, dateAccomplished = %s, projectID = %s
        WHERE taskID = %s
    """
    
    values = (
        updatedTask["taskID"],
        updatedTask["taskName"],
        updatedTask.get("shortDescrip"),
        updatedTask["currentStatus"],
        updatedTask.get("dueDate"),
        updatedTask.get("dateAccomplished"),
        updatedTask["projectID"],
        originalID
    )
    
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()

def deleteTask(taskID: str) -> None:
    conn = getConnection()
    cursor = conn.cursor()
    
    sql = "DELETE FROM task WHERE taskID = %s"
    
    cursor.execute(sql, (taskID,))
    conn.commit()
    cursor.close()
    conn.close()

def getAllTasks() -> list[dict]:
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)
    
    sql = "SELECT * FROM task"
    
    cursor.execute(sql)
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return tasks

def getTaskByID(taskID: str) -> dict | None:
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)
    
    sql = "SELECT * FROM task WHERE taskID = %s"
    
    cursor.execute(sql, (taskID,))
    task = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return task

def taskExists(taskID: str) -> bool:
    conn = getConnection()
    cursor = conn.cursor()
    
    sql = "SELECT 1 FROM task WHERE taskID = %s"
    
    cursor.execute(sql, (taskID,))
    exists = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    
    return exists

def searchTasks(keyword: str) -> list[dict]:
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)
    
    sql = """
        SELECT * FROM task
        WHERE taskName LIKE %s OR shortDescrip LIKE %s OR currentStatus LIKE %s
    
    """
    like = f"%{keyword}%"
    cursor.execute(sql, (like, like, like))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return results

# --- TaskMember (Assignment) --- #

def assignMemberToTask(taskID: str, memberID: str, dateAssigned:str | None = None) -> None:
    conn = getConnection()
    cursor = conn.cursor()
    
    sql = "INSERT INTO taskMember (taskID, memberID, dateAssigned) VALUES (%s, %s, %s)"
    
    cursor.execute(sql, (taskID, memberID, dateAssigned))
    conn.commit()
    cursor.close()
    conn.close()

def removeMemberFromTask(taskID: str, memberID: str):
    conn = getConnection()
    cursor = conn.cursor()
    
    sql = "DELETE FROM taskMember WHERE taskID = %s AND memberID = %s"
    
    cursor.execute(sql, (taskID, memberID))
    conn.commit()
    cursor.close()
    conn.close()

def getMembersForTask(taskID: str) -> list[dict]:
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)
    
    sql = """
        SELECT m.* FROM members m
        JOIN taskMember tm ON m.memberID = tm.memberID
        WHERE tm.taskID = %s
    """
    
    cursor.execute(sql, (taskID,))
    members = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return members

def getTasksForMember(memberID: str) -> list[dict]:
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)
    
    sql = """
        SELECT t.* FROM task t
        JOIN taskMember tm ON t.taskID = tm.taskID
        WHERE tm.memberID = %s
    """
    
    cursor.execute(sql, (memberID,))
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return tasks

# --- Task Status and Accomplishment ---

def updateTaskStatus(taskID: str, status: str) -> None:
    conn = getConnection()
    cursor = conn.cursor()
    
    sql = "UPDATE task SET currentStatus = %s WHERE taskID = %s"
    
    cursor.execute(sql, (status, taskID))
    conn.commit()
    cursor.close()
    conn.close()

def setTaskAccomplished(taskID: str, dateAccomplished) -> None:
    conn = getConnection()
    cursor = conn.cursor()
    
    sql = "UPDATE task SET dateAccomplished = %s, currentStatus = 'Completed' WHERE taskID = %s"
    
    cursor.execute(sql, (dateAccomplished, taskID))
    conn.commit()
    cursor.close()
    conn.close()

def getOverdueTasks(current_datetime) -> list[dict]:
    conn = getConnection()
    cursor = conn.cursor(dictionary=True)
    
    sql = """
        SELECT * FROM task
        WHERE dueDate < %s AND (currentStatus != 'Completed' OR currentStatus IS NULL)
    """
    
    cursor.execute(sql, (current_datetime,))
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return tasks
