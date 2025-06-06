from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.application.dependencies.database import get_db
from src.application.dependencies.service import get_post_service
from src.domain.services.blog_post import BlogPostService
from src.presentation.schemas.blog_post import (
    BlogPostCreate,
    BlogPostListItem,
    BlogPostResponse,
)

router = APIRouter(tags=["Posts"])


@router.get("/", response_model=List[BlogPostListItem])
def list_blog_posts(
    service: BlogPostService = Depends(get_post_service),
    db: Session = Depends(get_db),
):
    return service.list_posts(db)


@router.get("/{post_id}", response_model=BlogPostResponse)
def get_blog_post(
    post_id: int,
    service: BlogPostService = Depends(get_post_service),
    db: Session = Depends(get_db),
):
    return service.get_post_detail(db, post_id)


@router.post("/", response_model=BlogPostResponse, status_code=status.HTTP_201_CREATED)
def create_blog_post(
    data: BlogPostCreate,
    service: BlogPostService = Depends(get_post_service),
    db: Session = Depends(get_db),
):
    return service.create_post(db, data)
