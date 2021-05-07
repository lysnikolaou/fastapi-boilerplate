import uuid
from typing import Generator

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from rook.db.session import SessionLocal
from rook.usecases.user.user_crud import create_user as create_user_crud

app = FastAPI()


class RootResponse(BaseModel):
    message: str


class UsersCreateRequest(BaseModel):
    email: str


class UsersCreateResponse(BaseModel):
    user_id: uuid.UUID
    email: str


def get_db() -> Generator[Session, None, None]:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exception: RequestValidationError
) -> JSONResponse:
    data = {"errors": exception.errors()}
    return JSONResponse(content=data, status_code=400)


@app.get("/", response_model=RootResponse)
async def root() -> RootResponse:
    return RootResponse(message="hello world")


@app.post(
    "/users",
    response_model=UsersCreateResponse,
    status_code=201,
)
async def create_user(
    *, db: Session = Depends(get_db), user: UsersCreateRequest
) -> UsersCreateResponse:
    new_user, created = create_user_crud(db, user.email)
    if not created:
        raise HTTPException(
            status_code=409, detail=f"A user with the email {user.email} already exists"
        )
    return UsersCreateResponse(user_id=new_user.id, email=new_user.email)
