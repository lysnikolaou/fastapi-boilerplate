import uuid

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.ext.declarative import declared_attr

from rook.db.base_class import Base


class User(Base):
    @declared_attr
    def __tablename__(cls) -> str:
        return "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(TEXT, unique=True, index=True, nullable=False)

    @property
    def id(self) -> str:
        return self.user_id
