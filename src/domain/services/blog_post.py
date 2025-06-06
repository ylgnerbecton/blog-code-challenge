from typing import List, Optional

from sqlalchemy.orm import Session

from src.domain.services.base import BaseService
from src.infrastructure.repositories.blog_post import BlogPostRepository
from src.presentation.schemas.blog_post import (
    BlogPostCreate,
    BlogPostListItem,
    BlogPostResponse,
)
from src.presentation.schemas.comment import CommentResponse


class BlogPostService(BaseService):
    def __init__(self, repository: BlogPostRepository = None):
        self.repository = repository or BlogPostRepository()
        super().__init__(repository=self.repository)

    def list_posts(self, db: Session) -> List[BlogPostListItem]:
        posts_with_counts = self.repository.get_all_with_comment_count(db)
        return [
            BlogPostListItem(
                id=post.id,
                title=post.title,
                comments_count=comments_count,
            )
            for post, comments_count in posts_with_counts
        ]

    def create_post(self, db: Session, data: BlogPostCreate) -> BlogPostResponse:
        created = self.create(db, data)
        return BlogPostResponse(
            id=created.id,
            title=created.title,
            content=created.content,
            comments=[],
        )

    def get_post_detail(self, db: Session, post_id: int) -> Optional[BlogPostResponse]:
        post = self.repository.get_with_comments(db, post_id)
        if not post:
            return None

        return BlogPostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            comments=[CommentResponse(id=c.id, content=c.content) for c in post.comments],
        )
