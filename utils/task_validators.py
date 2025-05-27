from config.db_config import getConnection

# ADD TASK VALIDATION FUNCTIONS HERE
def task_exists(table: str, column: str, value) -> bool:
    conn = getConnection()
    cursor = conn.cursor()
    sql = f"SELECT COUNT(*) FROM {table} WHERE {column} = %s"
    cursor.execute(sql, (value,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0

def is_unique_taskID(taskID):
    return not task_exists('task', 'taskID', taskID)

def uniqueTask(taskID):
    if not is_unique_taskID(taskID):
        return f"Task ID {taskID} already exists."
    return None

# EDIT TASK VALIDATION FUNCTIONS HERE
def task_exists_excluding(table: str, column: str, value, exclude_column: str, exclude_value) -> bool:
    conn = getConnection()
    cursor = conn.cursor()
    sql = f"SELECT COUNT(*) FROM {table} WHERE {column} = %s AND {exclude_column} <> %s"
    cursor.execute(sql, (value, exclude_value))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0

def uniqueEditTask(new_id: str, original_id: str) -> str | None:
    if task_exists_excluding('task', 'taskID', new_id, 'taskID', original_id):
        return f"Task ID {new_id} already exists."
    return None