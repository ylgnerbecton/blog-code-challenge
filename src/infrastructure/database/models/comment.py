from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from src.infrastructure.database import BaseModel


class Comment(BaseModel):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)

    post_id = Column(Integer, ForeignKey("blog_posts.id", ondelete="CASCADE"), nullable=False)
    post = relationship("BlogPost", back_populates="comments")
