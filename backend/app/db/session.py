from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings


class Base(DeclarativeBase):
    pass


_engine = None
_session_factory = None
_db_available = False
_db_error: str | None = None


def init_database() -> None:
    """Connect and create tables when PostgreSQL is enabled and reachable."""
    global _engine, _session_factory, _db_available, _db_error
    settings = get_settings()
    if not settings.database_enabled:
        _db_available = False
        _db_error = "Database persistence is disabled."
        return
    try:
        _engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)
        with _engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        from app.models import analysis as _analysis_model  # noqa: F401

        Base.metadata.create_all(_engine)
        _session_factory = sessionmaker(bind=_engine, autoflush=False, autocommit=False, future=True)
        _db_available = True
        _db_error = None
    except Exception as exc:  # noqa: BLE001
        _engine = None
        _session_factory = None
        _db_available = False
        _db_error = str(exc)


def database_status() -> dict:
    return {"enabled": get_settings().database_enabled, "available": _db_available, "error": _db_error}


def get_session() -> Generator[Session, None, None]:
    if not _session_factory:
        raise RuntimeError("Database is not available.")
    session = _session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
