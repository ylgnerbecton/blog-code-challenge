from src.infrastructure.repositories.comment import CommentRepository
from src.infrastructure.repositories.blog_post import BlogPostRepository


def test_create_comment(db_session):
    post_repo = BlogPostRepository()
    comment_repo = CommentRepository()

    post = post_repo.create(db_session, {"title": "Post for comment", "content": "..."})
    comment = comment_repo.create(
        db_session, {"post_id": post.id, "content": "Nice post"}
    )

    assert comment.id is not None
    assert comment.post_id == post.id
    assert comment.content == "Nice post"


def test_get_comment_by_id(db_session):
    comment_repo = CommentRepository()
    comment = comment_repo.create(db_session, {"post_id": 1, "content": "Hello"})

    fetched = comment_repo.get_by_id(db_session, comment.id)

    assert fetched.id == comment.id
    assert fetched.content == "Hello"


def test_get_all_comments(db_session):
    comment_repo = CommentRepository()
    comment_repo.create(db_session, {"post_id": 1, "content": "Comment 1"})
    comment_repo.create(db_session, {"post_id": 1, "content": "Comment 2"})

    all_comments = comment_repo.get_all(db_session)

    assert len(all_comments) >= 2
