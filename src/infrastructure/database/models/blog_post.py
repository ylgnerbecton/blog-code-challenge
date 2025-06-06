from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from src.infrastructure.database import BaseModel


class BlogPost(BaseModel):
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)

    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
