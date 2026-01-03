"""Simple SQLite-backed task storage.

This module provides a tiny API for storing todo tasks in a local
SQLite database. Public functions are typed and documented so they can be
used easily by other modules and tests.

Data model:
- id: integer primary key
- description: text
- done: integer (0 or 1)
"""

import sqlite3
from contextlib import contextmanager
from typing import Iterator, List, Tuple

DB_NAME: str = "tasks.db"


@contextmanager
def get_db_connection() -> Iterator[sqlite3.Connection]:
    """Context manager that yields a SQLite connection and closes it.

    Yields:
        sqlite3.Connection: open SQLite connection to :data:`DB_NAME`.
    """
    conn = sqlite3.connect(DB_NAME)
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    """Create the `tasks` table if it does not already exist.

    This is safe to call multiple times.
    """
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


def add_task(desc: str) -> None:
    """Insert a new task with the given description.

    Args:
        desc: Task description text. Leading/trailing whitespace should be
            stripped by the caller if desired.
    """
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks(description) VALUES (?)", (desc,))
        conn.commit()


def get_tasks() -> List[Tuple[int, str, int]]:
    """Return all tasks as a list of tuples.

    Returns:
        A list of `(id, description, done)` tuples where `done` is 0 or 1.
    """
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, description, done FROM tasks")
        return cur.fetchall()


def delete_task(task_id: int) -> None:
    """Delete task with the given id.

    Args:
        task_id: Primary key of the task to remove.
    """
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()


def toggle_done(task_id: int, current: int) -> None:
    """Flip the `done` state for a task.

    Args:
        task_id: Primary key of the task to update.
        current: Current value of `done` (0 or 1). The function will set the
            column to the opposite value.
    """
    with get_db_connection() as conn:
        cur = conn.cursor()
        new = 0 if current else 1
        cur.execute("UPDATE tasks SET done = ? WHERE id = ?", (new, task_id))
        conn.commit()
