import os
import sys

sys.path.insert(0, os.getcwd())

import app.db as db

def test_db_crud(tmp_path):
    db.DB_NAME = str(tmp_path / "test_tasks.db")
    db.reset_engine()

    db.init_db()
    tasks = db.get_tasks()
    assert tasks == []

    db.add_task("test task")
    tasks = db.get_tasks()
    assert len(tasks) == 1

    task_id, desc, done, created_at = tasks[0]
    assert desc == "test task"
    assert done == 0
    assert len(created_at) == 16

    db.toggle_done(task_id, True)
    tasks = db.get_tasks()
    assert tasks[0][2] == 1

    db.delete_task(task_id)
    tasks = db.get_tasks()
    assert tasks == []

def test_clear_tasks(tmp_path):
    db.DB_NAME = str(tmp_path / "test_tasks.db")
    db.reset_engine()

    db.init_db()
    db.add_task("a")
    db.add_task("b")

    tasks = db.get_tasks()
    assert len(tasks) == 2

    db.clear_tasks()
    tasks = db.get_tasks()
    assert tasks == []
