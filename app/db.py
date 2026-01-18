import os
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, List, Tuple

from sqlalchemy import (
    Boolean,
    Integer,
    String,
    DateTime,
    create_engine,
    select,
    func,
)
from sqlalchemy.engine import Engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    sessionmaker,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = REPO_ROOT / "data" / "tasks.db"
DB_NAME: str = os.getenv("TDL_DB_PATH", str(DEFAULT_DB_PATH))


def _ensure_parent_dir(db_path: str) -> None:
    """Creates parent directory for the database file if it does not exist."""
    Path(db_path).expanduser().resolve().parent.mkdir(
        parents=True,
        exist_ok=True,
    )


class Base(DeclarativeBase):
    """Base class for ORM models."""


class Task(Base):
    """Model representing a single task in the database."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    description: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    done: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    created_at: Mapped[object] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.datetime("now", "localtime"),
    )

    def __repr__(self) -> str:
        """Return string representation of Task object."""
        return (
            f"Task(id={self.id}, "
            f"description={self.description!r}, "
            f"done={self.done})"
        )


def _sqlite_url_from_path(db_path: str) -> str:
    """Create SQLite database URL from file path."""
    p = Path(db_path).expanduser().resolve()
    return f"sqlite:///{p.as_posix()}"


def get_engine() -> Engine:
    """Create and return database engine."""
    _ensure_parent_dir(DB_NAME)
    url = _sqlite_url_from_path(DB_NAME)
    return create_engine(
        url,
        future=True,
        echo=False,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
    )


##################### changes made with help of ChatGPT #####################
_engine: Engine | None = None
SessionLocal: sessionmaker[Session] | None = None


def reset_engine() -> None:
    """Reset database engine (used mainly in tests)."""
    global _engine, SessionLocal
    _engine = None
    SessionLocal = None


def _ensure_engine() -> None:
    """Ensure that database engine and session factory are initialized."""
    global _engine, SessionLocal

    if _engine is None or SessionLocal is None:
        _engine = get_engine()
        SessionLocal = sessionmaker(
            bind=_engine,
            autoflush=False,
            autocommit=False,
            future=True,
        )
#############################################################################


@contextmanager
def get_session() -> Iterator[Session]:
    """Provide a database session as a context manager."""
    _ensure_engine()
    assert SessionLocal is not None

    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db() -> None:
    """Create database tables if they do not exist."""
    _ensure_engine()
    assert _engine is not None
    Base.metadata.create_all(bind=_engine)


def add_task(desc: str) -> None:
    """Add a new task to the database."""
    desc = (desc or "").strip()
    if not desc:
        return

    with get_session() as session:
        session.add(
            Task(
                description=desc,
                done=False,
            )
        )


def get_tasks() -> List[Tuple[int, str, int, str]]:
    """Return all tasks from the database.

    Returns:
        List of tuples (id, description, done, created_at)
    """
    with get_session() as session:
        stmt = select(Task).order_by(Task.id.asc())
        tasks = session.scalars(stmt).all()

        return [
            (
                t.id,
                t.description,
                1 if t.done else 0,
                t.created_at.strftime("%Y-%m-%d %H:%M"),
            )
            for t in tasks
        ]


def delete_task(task_id: int) -> None:
    """Delete task with given ID."""
    with get_session() as session:
        task = session.get(Task, task_id)
        if task is None:
            return
        session.delete(task)


def toggle_done(task_id: int, new_value: bool) -> None:
    """Change task completion status."""
    with get_session() as session:
        task = session.get(Task, task_id)
        if task is None:
            return
        task.done = bool(new_value)


def clear_tasks() -> None:
    """Remove all tasks from the database."""
    with get_session() as session:
        session.query(Task).delete()
