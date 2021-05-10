from __future__ import annotations

from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session

from rook.core.exceptions import FirebaseException, NonUniqueEmailException
from rook.models.user.user import User


def get_user_by_email(email: str, *, db: Session) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(email: str, password: str, *, db: Session) -> tuple[User, str]:
    user: auth.UserRecord
    try:
        user = auth.create_user(email=email, password=password)
    except auth.EmailAlreadyExistsError:
        user = auth.get_user_by_email(email)
    except FirebaseError as error:
        raise FirebaseException(error=error)

    try:
        with db.begin():
            if get_user_by_email(email, db=db) is not None:
                auth.delete_user(user.uid)
                raise NonUniqueEmailException()
            db_user = User(
                user_id=user.uid, email=user.email, created_by=user.uid, updated_by=user.uid
            )
            db.add(db_user)
    except DatabaseError:
        auth.delete_user(user.uid)
        raise

    db.refresh(db_user)
    token: bytes = auth.create_custom_token(user.uid)
    return db_user, token.decode()
