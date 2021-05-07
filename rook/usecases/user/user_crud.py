from __future__ import annotations

from sqlalchemy.orm import Session

from rook.models.user.user import User


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, email: str) -> tuple[User, bool]:
    created = False
    user = get_user_by_email(db, email)
    if user is None:
        user = User(email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
        created = True
    return user, created
