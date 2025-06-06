from fastapi import APIRouter

from src.presentation.views import blog_post, comment, health

router = APIRouter()

router.include_router(health.router, prefix="/health", tags=["Health"])
router.include_router(blog_post.router, prefix="/posts", tags=["Posts"])
router.include_router(comment.router, prefix="/comments", tags=["Comments"])
