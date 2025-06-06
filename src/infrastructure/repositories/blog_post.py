from typing import List, Tuple

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.infrastructure.database.models.blog_post import BlogPost
from src.infrastructure.database.models.comment import Comment
from src.infrastructure.repositories.base import BaseRepository


class BlogPostRepository(BaseRepository[BlogPost]):
    def __init__(self):
        super().__init__(BlogPost)

    def get_all_with_comment_count(self, db: Session) -> List[Tuple[BlogPost, int]]:
        return (
            db.query(BlogPost, func.count(Comment.id).label("comments_count"))
            .outerjoin(Comment)
            .group_by(BlogPost.id)
            .all()
        )

    def get_with_comments(self, db: Session, post_id: int) -> BlogPost | None:
        return db.query(BlogPost).filter(BlogPost.id == post_id).first()
