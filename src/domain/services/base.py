from typing import Generic, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.infrastructure.repositories.base import BaseRepository

ModelType = TypeVar("ModelType")


class BaseService(Generic[ModelType]):
    def __init__(
        self,
        repository: BaseRepository[ModelType],
    ):
        self.repository = repository

    def get_all(self, db: Session):
        return self.repository.get_all(db)

    def get_by_id(self, db: Session, obj_id: int):
        return self.repository.get_by_id(db, obj_id)

    def create(
        self,
        db: Session,
        obj_in: Union[BaseModel, dict],
    ):
        if isinstance(obj_in, BaseModel):
            obj_in = obj_in.model_dump(mode="json", exclude_unset=True)
        created = self.repository.create(db, obj_in)

        return created

    def update(
        self,
        db: Session,
        obj_id: int,
        obj_in: Union[BaseModel, dict],
    ):
        db_obj = self.get_by_id(db, obj_id)
        if isinstance(obj_in, BaseModel):
            obj_in = obj_in.model_dump(mode="json", exclude_unset=True)
        updated = self.repository.update(db, db_obj, obj_in)

        return updated
