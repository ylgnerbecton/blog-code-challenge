from sqlalchemy import Column, DateTime
from sqlalchemy.orm import as_declarative, declared_attr

from src.application.utils.general import get_current_time


@as_declarative()
class BaseModel:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    created_at = Column(DateTime(timezone=True), default=get_current_time, nullable=False, index=True)
    updated_at = Column(
        DateTime(timezone=True),
        default=get_current_time,
        onupdate=get_current_time,
        nullable=False,
        index=True,
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={getattr(self, 'id', None)})>"

    @classmethod
    def from_json(cls, data):
        keys = {column.name for column in cls.__table__.columns}
        return cls(**{k: v for k, v in data.items() if k in keys})
