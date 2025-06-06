from sqlalchemy.orm import Session

from src.domain.entities.comment import CommentEntity
from src.domain.services.base import BaseService
from src.infrastructure.repositories.comment import CommentRepository
from src.presentation.schemas.comment import CommentCreate, CommentResponse


class CommentService(BaseService):
    def __init__(self, repository: CommentRepository = None):
        self.repository = repository or CommentRepository()
        super().__init__(repository=self.repository)

    def add_comment(self, db: Session, post_id: int, data: CommentCreate) -> CommentResponse:
        comment_entity = CommentEntity(post_id=post_id, content=data.content)

        created = self.create(db, comment_entity.__dict__)

        return CommentResponse(id=created.id, content=created.content)

    def get_all_by_post_id(self, db: Session, post_id: int):
        comments = self.repository.get_by_post_id(db, post_id)
        return [CommentResponse(id=c.id, content=c.content) for c in comments]

    def get_by_id_and_post(self, db: Session, comment_id: int, post_id: int):
        comment = self.repository.get_by_id_and_post(db, comment_id, post_id)
        if comment:
            return CommentResponse(id=comment.id, content=comment.content)
        return None
