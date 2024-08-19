import sqlite3

def create_database():
    conn = sqlite3.connect('knowledge_graph.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tuples (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT,
        relation TEXT,
        value TEXT,
        file INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT,
        type_of_key TEXT,
        type_of_value TEXT
    )
    ''')

    conn.commit()
    conn.close()

create_database()


