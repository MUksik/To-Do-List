# Test CRUD db:
# sprawdza inicjalizację bazy danych, dodawanie zadania,
# zmianę statusu (done) oraz usuwanie, używając tymczasowej bazy

import os
import sys

sys.path.insert(0, os.getcwd())

import app.db as db

def test_db_crud(tmp_path):
    db.DB_NAME = str(tmp_path / "test_tasks.db")

    db.init_db()
    tasks = db.get_tasks()
    assert isinstance(tasks, list)
    assert tasks == []

    db.add_task("test task")
    tasks = db.get_tasks()
    assert len(tasks) == 1
    task_id, desc, done = tasks[0]
    assert desc == "test task"
    assert done == 0

    db.toggle_done(task_id, 0)
    tasks = db.get_tasks()
    assert tasks[0][2] == 1

    db.delete_task(task_id)
    tasks = db.get_tasks()
    assert tasks == []
