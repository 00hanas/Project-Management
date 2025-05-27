from PyQt6.QtCore import QDate
from config.db_config import getConnection

def getCalendarEvents():
    connection = getConnection()
    cursor = connection.cursor()

    sql = """
        SELECT projectName AS title, endDate AS date, 'project' AS type FROM project WHERE endDate IS NOT NULL
        UNION
        SELECT taskName AS title, dueDate AS date, 'task' AS type FROM task WHERE dueDate IS NOT NULL
    """

    cursor.execute(sql)

    events = []
    for title, date, type_ in cursor.fetchall():
        if date:  # Ensure date is not None
            qdate = QDate.fromString(date.strftime('%Y-%m-%d'), 'yyyy-MM-dd')
            events.append((qdate, title, type_))

    cursor.close()
    connection.close()
    return events

def getTotalProjectCount():
    connection = getConnection()
    cursor = connection.cursor()

    sql = "SELECT COUNT(*) FROM project"
    cursor.execute(sql)

    total_count = cursor.fetchone()[0]

    cursor.close()
    connection.close()
    return total_count

def getTotalTaskCount():
    connection = getConnection()
    cursor = connection.cursor()

    sql = "SELECT COUNT(*) FROM task"
    cursor.execute(sql)

    total_count = cursor.fetchone()[0]

    cursor.close()
    connection.close()
    return total_count

def getTotalMemberCount():
    connection = getConnection()
    cursor = connection.cursor()

    sql = "SELECT COUNT(*) FROM members"
    cursor.execute(sql)

    total_count = cursor.fetchone()[0]

    cursor.close()
    connection.close()
    return total_count

def getAllProjectsTasksMembers(keyword: str, search_by: str) -> list[dict]:
    try:
        conn = getConnection()
        cursor = conn.cursor()
        keyword_like = f"%{keyword}%"
        results = []

        # Normalize the search_by parameter
        search_by = search_by.lower().strip() if search_by else ""

        cursor.execute("""SELECT taskID, taskName FROM task WHERE taskID LIKE %s OR taskName LIKE %s""", (keyword_like, keyword_like))
        rows = cursor.fetchall()
        for row in rows:
            results.append({'type': 'task', 'id': row[0], 'label': row[1]})
        # Search projects
        if not search_by or "projects" in search_by:
            cursor.execute("""
                SELECT projectID, projectName 
                FROM project 
                WHERE projectID LIKE %s OR projectName LIKE %s
            """, (keyword_like, keyword_like))
            for row in cursor.fetchall():
                results.append({'type': 'project', 'id': row[0], 'label': row[1]})

        # Search tasks
        if not search_by or "tasks" in search_by:
            cursor.execute("""
                SELECT taskID, taskName 
                FROM task 
                WHERE taskID LIKE %s OR taskName LIKE %s
            """, (keyword_like, keyword_like))
            for row in cursor.fetchall():
                results.append({'type': 'task', 'id': row[0], 'label': row[1]})

        # Search members
        if not search_by or "members" in search_by:
            cursor.execute("""
                SELECT memberID, fullname, email 
                FROM members 
                WHERE memberID LIKE %s OR fullname LIKE %s OR email LIKE %s
            """, (keyword_like, keyword_like, keyword_like))
            for row in cursor.fetchall():
                results.append({'type': 'member', 'id': row[0], 'label': row[1]})


        return results

    except Exception as e:
        print(f"[ERROR] Database error: {e}")
        return []
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass



