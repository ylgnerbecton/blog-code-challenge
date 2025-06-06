from sqlalchemy.orm import Session

from src.infrastructure.database.models.comment import Comment
from src.infrastructure.repositories.base import BaseRepository


class CommentRepository(BaseRepository[Comment]):
    def __init__(self):
        super().__init__(Comment)

    def get_by_post_id(self, db: Session, post_id: int) -> list[Comment]:
        return db.query(Comment).filter(Comment.post_id == post_id).all()

    def get_by_id_and_post(self, db: Session, comment_id: int, post_id: int) -> Comment | None:
        return db.query(Comment).filter(Comment.id == comment_id, Comment.post_id == post_id).first()
