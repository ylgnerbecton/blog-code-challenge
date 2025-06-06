from typing import Generic, Type, TypeVar

from sqlalchemy.orm import Session

from src.infrastructure.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_by_id(self, db: Session, obj_id: int) -> ModelType | None:
        return db.query(self.model).filter(self.model.id == obj_id).first()

    def get_all(self, db: Session) -> list[ModelType]:
        return db.query(self.model).all()

    def create(self, db: Session, obj_in: dict) -> ModelType:
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: ModelType, obj_in: dict) -> ModelType:
        for key, value in obj_in.items():
            setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, obj_id: int) -> ModelType | None:
        obj = self.get_by_id(db, obj_id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
