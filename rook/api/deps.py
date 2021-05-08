from typing import Generator

from sqlalchemy.orm import Session

from rook.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
