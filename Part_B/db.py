import sqlite3

def connect_db():
    connection=sqlite3.connect('tesreco.db')
    return connection

def create_db():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interns(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        domain TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        intern_id INTEGER,
        date TEXT,
        status TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mentors(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        intern_id INTEGER,
        mentor_name TEXT,
        FOREIGN KEY(intern_id) REFERENCES interns(id)
    )
    """)

    connection.commit()
    connection.close()
