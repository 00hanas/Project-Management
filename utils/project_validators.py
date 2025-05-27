from config.db_config import getConnection

# ADD PROJECT VALIDATION FUNCTIONS HERE
def project_exists(table: str, column: str, value) -> bool:
    conn = getConnection()
    cursor = conn.cursor()
    sql = f"SELECT COUNT(*) FROM {table} WHERE {column} = %s"
    cursor.execute(sql, (value,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0

def is_unique_projectID(projectID):
    return not project_exists('project', 'projectID', projectID)

def uniqueProject(projectID):
    if not is_unique_projectID(projectID):
        return f"Project ID {projectID} already exists."
    return None

# EDIT PROJECT VALIDATION FUNCTIONS HERE
def project_exists_excluding(table: str, column: str, value, exclude_column: str, exclude_value) -> bool:
    conn = getConnection()
    cursor = conn.cursor()
    sql = f"SELECT COUNT(*) FROM {table} WHERE {column} = %s AND {exclude_column} <> %s"
    cursor.execute(sql, (value, exclude_value))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0

def uniqueEditProject(new_id: str, original_id: str) -> str | None:
    if project_exists_excluding('project', 'projectID', new_id, 'projectID', original_id):
        return f"Project ID {new_id} already exists."
    return None