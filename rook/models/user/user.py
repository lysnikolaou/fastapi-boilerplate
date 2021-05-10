from dataclasses import dataclass
from typing import Any

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.ext.declarative import declared_attr

from rook.db.base_class import Auditable


@dataclass
class FirebaseUser:
    user_id: str
    email: str
    claims: dict[str, Any]


class User(Auditable):
    @declared_attr
    def __tablename__(cls) -> str:
        return "users"

    user_id = Column(TEXT, primary_key=True, index=True)
    email = Column(TEXT, unique=True, index=True, nullable=False)
    last_login_at = Column(DateTime(timezone=True))

    @property
    def id(self) -> str:
        return self.user_id
