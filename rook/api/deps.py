from typing import Generator

from fastapi import Depends
from firebase_admin import auth
from sqlalchemy.orm import Session

from rook.core.exceptions import AuthenticationFailed
from rook.core.security import BearerAuth
from rook.db.session import SessionLocal
from rook.models.user.user import FirebaseUser


def get_db() -> Generator[Session, None, None]:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(BearerAuth)) -> FirebaseUser:
    try:
        payload = auth.verify_id_token(token)
    except auth.ExpiredIdTokenError:
        raise AuthenticationFailed("Authentication token is expired")
    except (auth.InvalidIdTokenError, auth.RevokedIdTokenError):
        raise AuthenticationFailed("Authentication token is invalid")

    uid: str = payload["uid"]
    try:
        user: auth.UserRecord = auth.get_user(uid)
    except auth.UserNotFoundError:
        raise AuthenticationFailed("Authentication token is not linked to a user")

    return FirebaseUser(user_id=user.uid, email=user.email, claims=user.custom_claims)
