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

