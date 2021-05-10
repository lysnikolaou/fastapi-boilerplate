from datetime import datetime
from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import TEXT, DateTime


@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Auditable(Base):
    __abstract__ = True

    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
    updated_at = Column(
        DateTime(timezone=True), default=datetime.now, onupdate=datetime.now, nullable=False
    )
    created_by = Column(TEXT, nullable=False)
    updated_by = Column(TEXT, nullable=False)
