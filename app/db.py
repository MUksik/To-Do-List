import os
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, List, Tuple

from sqlalchemy import Boolean, Integer, String, create_engine, select, DateTime, func
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = REPO_ROOT / "data" / "tasks.db"
DB_NAME: str = os.getenv("TDL_DB_PATH", str(DEFAULT_DB_PATH))


def _ensure_parent_dir(db_path: str) -> None:
    Path(db_path).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    done: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[object] = mapped_column(DateTime, nullable=False, server_default=func.datetime("now", "localtime"))

    def __repr__(self) -> str:
        return f"Task(id={self.id}, description={self.description!r}, done={self.done})"


def _sqlite_url_from_path(db_path: str) -> str:
    p = Path(db_path).expanduser().resolve()
    return f"sqlite:///{p.as_posix()}"


def get_engine() -> Engine:
    _ensure_parent_dir(DB_NAME)
    url = _sqlite_url_from_path(DB_NAME)
    return create_engine(url, future=True, echo=False, connect_args={"check_same_thread": False}, pool_pre_ping=True)


############################## zmiany wykonane przy pomocy ChataGPT ##############################
_engine: Engine | None = None
SessionLocal: sessionmaker[Session] | None = None


def reset_engine() -> None:
    global _engine, SessionLocal
    _engine = None
    SessionLocal = None


def _ensure_engine() -> None:
    global _engine, SessionLocal
    if _engine is None or SessionLocal is None:
        _engine = get_engine()
        SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False, future=True)
##################################################################################################


@contextmanager
def get_session() -> Iterator[Session]:
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
    _ensure_engine()
    assert _engine is not None
    Base.metadata.create_all(bind=_engine)


def add_task(desc: str) -> None:
    desc = (desc or "").strip()
    if not desc:
        return
    with get_session() as session:
        session.add(Task(description=desc, done=False))


def get_tasks() -> List[Tuple[int, str, int, str]]:
    with get_session() as session:
        stmt = select(Task).order_by(Task.id.asc())
        tasks = session.scalars(stmt).all()
        return [(t.id, t.description, 1 if t.done else 0, t.created_at.strftime("%Y-%m-%d %H:%M")) for t in tasks]


def delete_task(task_id: int) -> None:
    with get_session() as session:
        task = session.get(Task, task_id)
        if task is None:
            return
        session.delete(task)


def toggle_done(task_id: int, new_value: bool) -> None:
    with get_session() as session:
        task = session.get(Task, task_id)
        if task is None:
            return
        task.done = bool(new_value)

def clear_tasks() -> None:
    with get_session() as session:
        session.query(Task).delete()
