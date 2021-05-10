from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str


class UserCreateRequest(UserCreate):
    password: str


class UserCreateResponse(UserCreate):
    uid: str
    token: str
