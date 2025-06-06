from typing import List

from pydantic import BaseModel, ConfigDict

from src.presentation.schemas.comment import CommentResponse


class BlogPostBase(BaseModel):
    title: str
    content: str


class BlogPostCreate(BlogPostBase):
    pass


class BlogPostResponse(BlogPostBase):
    id: int
    comments: List[CommentResponse] = []

    model_config = ConfigDict(from_attributes=True)


class BlogPostListItem(BaseModel):
    id: int
    title: str
    comments_count: int

    model_config = ConfigDict(from_attributes=True)
