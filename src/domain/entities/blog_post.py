from dataclasses import dataclass, field
from typing import List

from src.domain.entities.comment import CommentEntity


@dataclass
class BlogPostEntity:
    id: int
    title: str
    content: str
    comments: List[CommentEntity] = field(default_factory=list)
