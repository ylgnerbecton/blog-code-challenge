import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from src.domain.services.blog_post import BlogPostService
from src.domain.services.comment import CommentService
from src.presentation.schemas.blog_post import BlogPostCreate, BlogPostResponse
from src.presentation.schemas.comment import CommentCreate, CommentResponse


@pytest.fixture
def mock_post_repository():
    return MagicMock()


@pytest.fixture
def mock_comment_repository():
    return MagicMock()


@pytest.fixture
def db_session():
    return MagicMock(spec=Session)


def test_create_blog_post(db_session, mock_post_repository):
    service = BlogPostService(repository=mock_post_repository)

    data = BlogPostCreate(title="My first post", content="Some content")

    mock_created = MagicMock()
    mock_created.id = 1
    mock_created.title = "My first post"
    mock_created.content = "Some content"
    mock_created.comments = []

    mock_post_repository.create.return_value = mock_created

    result = service.create_post(db_session, data)

    assert isinstance(result, BlogPostResponse)
    assert result.id == 1
    assert result.title == "My first post"
    assert result.content == "Some content"
    assert result.comments == []
    mock_post_repository.create.assert_called_once()


def test_get_post_detail(db_session, mock_post_repository):
    service = BlogPostService(repository=mock_post_repository)

    mock_post = MagicMock()
    mock_post.id = 1
    mock_post.title = "Post"
    mock_post.content = "Content"
    mock_post.comments = []

    mock_post_repository.get_with_comments.return_value = mock_post

    result = service.get_post_detail(db_session, 1)

    assert isinstance(result, BlogPostResponse)
    assert result.id == 1
    assert result.title == "Post"
    assert result.content == "Content"
    assert result.comments == []
    mock_post_repository.get_with_comments.assert_called_once_with(db_session, 1)


def test_add_comment_to_post(db_session, mock_comment_repository):
    service = CommentService(repository=mock_comment_repository)

    data = CommentCreate(content="Nice post!")

    mock_created = MagicMock()
    mock_created.id = 1
    mock_created.content = "Nice post!"

    mock_comment_repository.create.return_value = mock_created

    result = service.add_comment(db_session, post_id=1, data=data)

    assert isinstance(result, CommentResponse)
    assert result.id == 1
    assert result.content == "Nice post!"
    mock_comment_repository.create.assert_called_once()
