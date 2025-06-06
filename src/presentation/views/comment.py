from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.application.dependencies.database import get_db
from src.application.dependencies.service import get_comment_service
from src.domain.services.comment import CommentService
from src.presentation.schemas.comment import CommentCreate, CommentResponse

router = APIRouter(tags=["Comments"])


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def add_comment_to_post(
    post_id: int,
    data: CommentCreate,
    service: CommentService = Depends(get_comment_service),
    db: Session = Depends(get_db),
):
    return service.add_comment(db, post_id, data)


@router.get("/", response_model=List[CommentResponse])
def list_comments_for_post(
    post_id: int,
    service: CommentService = Depends(get_comment_service),
    db: Session = Depends(get_db),
):
    return service.get_all_by_post_id(db, post_id)


@router.get("/{comment_id}", response_model=CommentResponse)
def get_comment_by_id(
    post_id: int,
    comment_id: int,
    service: CommentService = Depends(get_comment_service),
    db: Session = Depends(get_db),
):
    return service.get_by_id_and_post(db, comment_id, post_id)
