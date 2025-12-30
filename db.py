import sqlite3
from contextlib import contextmanager

DB_NAME = "tasks.db"

@contextmanager
def get_db_connection():
    """Context Manager - automatyczne zamykanie połączenia DB"""
    conn = sqlite3.connect(DB_NAME)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                done INTEGER DEFAULT 0
            )
        """)
        conn.commit()

def add_task(desc: str):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks(description) VALUES (?)", (desc,))
        conn.commit()

def get_tasks():
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, description, done FROM tasks")
        return cur.fetchall()

def delete_task(task_id: int):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()

def toggle_done(task_id: int, current: int):
    with get_db_connection() as conn:
        cur = conn.cursor()
        new = 0 if current else 1
        cur.execute("UPDATE tasks SET done = ? WHERE id = ?", (new, task_id))
        conn.commit()
