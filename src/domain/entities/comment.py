from dataclasses import dataclass


@dataclass
class CommentEntity:
    content: str
    post_id: int
    id: int | None = None
