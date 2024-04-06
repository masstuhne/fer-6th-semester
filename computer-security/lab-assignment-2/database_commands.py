import sqlite3


def open_connection():
    connection = sqlite3.connect('user_database_final.db')
    cursor = connection.cursor()
    return connection, cursor


def close_connection(connection, cursor):
    connection.commit()
    cursor.close()
    connection.close()


def init_database():
    connection, cursor = open_connection()
    cursor.execute("CREATE TABLE IF NOT EXISTS users("
                   "uuid TEXT PRIMARY KEY, "
                   "username TEXT, "
                   "password BLOB, "
                   "force_change_password_req BOOL)")
    close_connection(connection, cursor)


# -------------------------------------------------------------------

init_database()

# -------------------------------------------------

def exists_user_by_username(username):
    connection, cursor = open_connection()
    cursor.execute("SELECT EXISTS(SELECT * FROM users WHERE username = ?)", (username, ))
    result = cursor.fetchone()[0]
    close_connection(connection, cursor)
    return result


def get_user_password(username):
    connection, cursor = open_connection()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username, ))
    result = cursor.fetchone()[0]
    close_connection(connection, cursor)
    return result


def get_user_force_req(username):
    connection, cursor = open_connection()
    cursor.execute("SELECT force_change_password_req FROM users WHERE username = ?", (username, ))
    result = cursor.fetchone()[0]
    close_connection(connection, cursor)
    return result


def add_user(uuid, username, password, force_password_change_required):
    connection, cursor = open_connection()
    cursor.execute("INSERT INTO users VALUES(?,?,?,?)",
                   (uuid, username, password, force_password_change_required))
    close_connection(connection, cursor)


def update_user_password(username, password):
    connection, cursor = open_connection()
    cursor.execute("UPDATE users SET password = ? WHERE username = ?",
                   (password, username))
    close_connection(connection, cursor)


def update_user_force_req(username, force_password_change_required):
    connection, cursor = open_connection()
    cursor.execute("UPDATE users SET force_change_password_req = ? WHERE username = ?",
                   (force_password_change_required, username))
    close_connection(connection, cursor)


def delete_user(username):
    connection, cursor = open_connection()
    cursor.execute("DELETE FROM users WHERE uuid = ?", (username, ))
    close_connection(connection, cursor)
