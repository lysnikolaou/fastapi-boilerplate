from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from rook.api.deps import get_db
from rook.api.schemas.user import UserCreateRequest, UserCreateResponse
from rook.usecases.user import user_crud

router = APIRouter()


@router.post("/", response_model=UserCreateResponse)
def create_user(user: UserCreateRequest, db: Session = Depends(get_db)) -> UserCreateResponse:
    user_db, token = user_crud.create_user(user.email, user.password, db=db)
    return UserCreateResponse(email=user_db.email, uid=user_db.id, token=token)
