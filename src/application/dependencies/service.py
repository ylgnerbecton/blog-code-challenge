from src.domain.services.blog_post import BlogPostService
from src.domain.services.comment import CommentService


def get_post_service() -> BlogPostService:
    return BlogPostService()


def get_comment_service() -> CommentService:
    return CommentService()
