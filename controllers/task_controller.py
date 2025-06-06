from config.db_config import getConnection
import pymysql.cursors


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
    
    try:
        # Update task info
        sql = """
            UPDATE task
            SET taskID = %s, taskName = %s, shortDescrip = %s,
                currentStatus = %s, dueDate = %s, dateAccomplished = %s, projectID = %s
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

        # Update project endDate if dateAccomplished changed and is the latest
        if updatedTask.get("dateAccomplished"):
            project_id = updatedTask["projectID"]
            cursor.execute("""
                SELECT MAX(dateAccomplished)
                FROM task
                WHERE projectID = %s AND dateAccomplished IS NOT NULL
            """, (project_id,))
            latest_completion = cursor.fetchone()[0]

            if latest_completion:
                cursor.execute("""
                    UPDATE project
                    SET endDate = %s
                    WHERE projectID = %s
                """, (latest_completion, project_id))

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
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
    cursor = conn.cursor(pymysql.cursors.DictCursor) #########################################################
    
    sql = "SELECT * FROM task"
    
    cursor.execute(sql)
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return tasks

def getTaskByID(taskID: str) -> dict | None:
    conn = getConnection()
    cursor = conn.cursor(pymysql.cursors.DictCursor) #########################################################
    
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

# In task_controller.py - update the searchTasks function
def searchTasks(keyword: str, search_by: str) -> list[dict]:
    if not keyword.strip():
        return []
        
    conn = getConnection()
    cursor = conn.cursor(pymysql.cursors.DictCursor) #########################################################
    
    keyword_like = f"%{keyword}%"
    
    # Use parameterized queries to prevent SQL injection
    if search_by == "Task ID":
        sql = "SELECT taskID FROM task WHERE taskID LIKE %s LIMIT 100"
        params = (keyword_like,)
    elif search_by == "Name":
        sql = "SELECT taskID FROM task WHERE taskName LIKE %s LIMIT 100"
        params = (keyword_like,)
    elif search_by == "Status":
        sql = "SELECT taskID FROM task WHERE currentStatus LIKE %s LIMIT 100"
        params = (keyword_like,)
    elif search_by == "Due Date":
        sql = "SELECT taskID FROM task WHERE DATE_FORMAT(dueDate, '%%Y-%%m-%%d') LIKE %s LIMIT 100"
        params = (keyword_like,)
    elif search_by == "Date Accomplished":
        sql = "SELECT taskID FROM task WHERE DATE_FORMAT(dateAccomplished, '%%Y-%%m-%%d') LIKE %s LIMIT 100"
        params = (keyword_like,)
    elif search_by == "Project":
        sql = "SELECT taskID FROM task WHERE projectID LIKE %s LIMIT 100"
        params = (keyword_like,)
    else:
        sql = """
            SELECT taskID FROM task 
            WHERE taskID LIKE %s 
               OR taskName LIKE %s  
               OR currentStatus LIKE %s
               OR DATE_FORMAT(dueDate, '%%Y-%%m-%%d') LIKE %s
               OR DATE_FORMAT(dateAccomplished, '%%Y-%%m-%%d') LIKE %s
               OR projectID LIKE %s
            LIMIT 100
        """
        params = (keyword_like,) * 6

    try:
        cursor.execute(sql, params)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def getAllTasksForSearch(task_ids: list[str]) -> list[tuple]:
    conn = getConnection()
    cursor = conn.cursor()

    if not task_ids:
        return []
    
    if isinstance(task_ids[0], dict):
        task_ids = [task['taskID'] for task in task_ids]

    placeholders = ', '.join(['%s'] * len(task_ids))
    sql = f"SELECT * FROM task WHERE taskID IN ({placeholders})"

    cursor.execute(sql, tuple(task_ids))
    tasks = cursor.fetchall()

    cursor.close()
    conn.close()
    return tasks

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
    cursor = conn.cursor(pymysql.cursors.DictCursor) #########################################################
    
    
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
    cursor = conn.cursor(pymysql.cursors.DictCursor) #########################################################
    
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
    
    try:
        # First update the task status
        sql = "UPDATE task SET currentStatus = %s WHERE taskID = %s"
        cursor.execute(sql, (status, taskID))
        
        # If status is being set to "Completed", we need to check if all tasks in the project are completed
        if status == "Completed":
            # Get the project ID for this task
            cursor.execute("SELECT projectID FROM task WHERE taskID = %s", (taskID,))
            result = cursor.fetchone()
            if result:
                project_id = result[0]
                
                # Check if there are any incomplete tasks in this project
                cursor.execute("""
                    SELECT COUNT(*) FROM task 
                    WHERE projectID = %s AND (currentStatus != 'Completed' OR currentStatus IS NULL)
                """, (project_id,))
                incomplete_tasks = cursor.fetchone()[0]
                
                if incomplete_tasks == 0:
                    # All tasks are completed, get the most recent completion date
                    cursor.execute("""
                        SELECT MAX(dateAccomplished) 
                        FROM task 
                        WHERE projectID = %s AND dateAccomplished IS NOT NULL
                    """, (project_id,))
                    latest_completion = cursor.fetchone()[0]
                    
                    if latest_completion:
                        # Update project end date to the most recent completion date
                        cursor.execute("""
                            UPDATE project 
                            SET endDate = %s 
                            WHERE projectID = %s
                        """, (latest_completion, project_id))
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def setTaskAccomplished(taskID: str, dateAccomplished) -> None:
    conn = getConnection()
    cursor = conn.cursor()
    
    try:
        # First update the task status and date accomplished
        sql = "UPDATE task SET dateAccomplished = %s, currentStatus = 'Completed' WHERE taskID = %s"
        cursor.execute(sql, (dateAccomplished, taskID))
        
        # Get the project ID for this task
        cursor.execute("SELECT projectID FROM task WHERE taskID = %s", (taskID,))
        result = cursor.fetchone()
        if result:
            project_id = result[0]
            
            # Check if there are any incomplete tasks in this project
            cursor.execute("""
                SELECT COUNT(*) FROM task 
                WHERE projectID = %s AND (currentStatus != 'Completed' OR currentStatus IS NULL)
            """, (project_id,))
            incomplete_tasks = cursor.fetchone()[0]
            
            if incomplete_tasks == 0:
                # All tasks are completed, get the most recent completion date
                cursor.execute("""
                    SELECT MAX(dateAccomplished) 
                    FROM task 
                    WHERE projectID = %s AND dateAccomplished IS NOT NULL
                """, (project_id,))
                latest_completion = cursor.fetchone()[0]
                
                if latest_completion:
                    # Update project end date to the most recent completion date
                    cursor.execute("""
                        UPDATE project 
                        SET endDate = %s 
                        WHERE projectID = %s
                    """, (latest_completion, project_id))
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def getOverdueTasks(current_datetime) -> list[dict]:
    conn = getConnection()
    cursor = conn.cursor(pymysql.cursors.DictCursor) #########################################################
    
    sql = """
        SELECT * FROM task
        WHERE dueDate < %s AND (currentStatus != 'Completed' OR currentStatus IS NULL)
    """
    
    cursor.execute(sql, (current_datetime,))
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return tasks

def getTasksByProjectID(projectID: str) -> list[dict]:
    """
    Retrieves all tasks associated with a given projectID.
    Returns a list of dictionaries, where each dictionary represents a task.
    """
    conn = getConnection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT taskID, taskName, currentStatus, dueDate FROM task WHERE projectID = %s ORDER BY taskID"
    try:
        cursor.execute(sql, (projectID,))
        tasks = cursor.fetchall()
        return tasks if tasks else []
    except Exception as e:
        print(f"Error fetching tasks for project {projectID}: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def sortTasks(sort_by: str, ascending: bool = True) -> list[dict]:
    conn = getConnection()
    cursor = conn.cursor(pymysql.cursors.DictCursor) #########################################################
    
    # Map UI sort options to database columns
    sort_mapping = {
        "Name": "taskName",
        "Task ID": "taskID",
        "Due Date": "dueDate",
        "Status": "currentStatus",
        "Project": "projectID",
        "Date Accomplished": "dateAccomplished"
    }
    
    if sort_by not in sort_mapping:
        sort_by = "taskName"  # Default sort
    
    order = "ASC" if ascending else "DESC"
    
    sql = f"SELECT * FROM task ORDER BY {sort_mapping[sort_by]} {order}"
    
    cursor.execute(sql)
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return tasks

# In task_controller.py
def getTasksByProject(project_id):
    conn = getConnection()
    cursor = conn.cursor()

    query = "SELECT * FROM task WHERE projectID = %s"
    cursor.execute(query, (project_id))
    result = cursor.fetchall()
    return [dict(zip([column[0] for column in cursor.description], row)) for row in result]