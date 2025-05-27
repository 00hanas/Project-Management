from config.db_config import getConnection

# ADD MEMBER VALIDATION FUNCTIONS HERE
def member_exists(table: str, column: str, value) -> bool:
    conn = getConnection()
    cursor = conn.cursor()
    sql = f"SELECT COUNT(*) FROM {table} WHERE {column} = %s"
    cursor.execute(sql, (value,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0

def is_unique_memberID(memberID):
    return not member_exists('members', 'memberID', memberID)

def uniqueMember(memberID):
    if not is_unique_memberID(memberID):
        return f"Student ID {memberID} already exists."
    return None

# EDIT MEMBER VALIDATION FUNCTIONS HERE
def member_exists_excluding(table: str, column: str, value, exclude_column: str, exclude_value) -> bool:
    conn = getConnection()
    cursor = conn.cursor()
    sql = f"SELECT COUNT(*) FROM {table} WHERE {column} = %s AND {exclude_column} <> %s"
    cursor.execute(sql, (value, exclude_value))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count > 0

def uniqueEditMember(new_id: str, original_id: str) -> str | None:
    if member_exists_excluding('members', 'memberID', new_id, 'memberID', original_id):
        return f"Member ID {new_id} already exists."
    return None