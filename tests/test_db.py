import app.db as db


def _setup_db(tmp_path, filename="test_tasks.db"):
    """Helper to configure a fresh database for each test run."""
    db.DB_NAME = str(tmp_path / filename)
    db.reset_engine()
    db.init_db()


def test_db_crud(tmp_path):
    """Test basic CRUD flow: create, read, update, delete."""
    _setup_db(tmp_path)

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
    """Test clearing all tasks from the database."""
    _setup_db(tmp_path)
    
    db.add_task("a")
    db.add_task("b")

    tasks = db.get_tasks()
    assert len(tasks) == 2

    db.clear_tasks()
    tasks = db.get_tasks()
    assert tasks == []


def test_add_task_ignores_empty_input(tmp_path):
    """Test that empty/blank task descriptions are not added."""
    _setup_db(tmp_path)

    db.add_task("")
    db.add_task("   ")
    db.add_task(None)

    tasks = db.get_tasks()
    assert tasks == []


def test_add_task_strips_whitespace(tmp_path):
    """Test that task descriptions are stripped of leading/trailing whitespace."""
    _setup_db(tmp_path)

    db.add_task("  abc  ")
    tasks = db.get_tasks()

    assert len(tasks) == 1
    assert tasks[0][1] == "abc"


def test_toggle_and_delete_missing_id(tmp_path):
    """Test toggling/deleting non-existing task IDs does not crash or change data."""
    _setup_db(tmp_path)

    db.add_task("x")
    tasks_before = db.get_tasks()
    assert len(tasks_before) == 1

    db.toggle_done(999999, True)
    db.delete_task(999999)

    tasks_after = db.get_tasks()
    assert tasks_after == tasks_before


def test_get_tasks_order_by_id(tmp_path):
    """Test that get_tasks returns tasks ordered by id ascending."""
    _setup_db(tmp_path)

    db.add_task("b")
    db.add_task("a")
    tasks = db.get_tasks()

    assert len(tasks) == 2
    assert tasks[0][0] < tasks[1][0]
    assert tasks[0][1] == "b"
    assert tasks[1][1] == "a"