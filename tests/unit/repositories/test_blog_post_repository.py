from src.infrastructure.repositories.blog_post import BlogPostRepository


def test_create_blog_post(db_session):
    repo = BlogPostRepository()
    post_data = {"title": "Test Post", "content": "Test content"}
    post = repo.create(db_session, post_data)

    assert post.id is not None
    assert post.title == "Test Post"
    assert post.content == "Test content"


def test_get_blog_post_by_id(db_session):
    repo = BlogPostRepository()
    created = repo.create(db_session, {"title": "Post", "content": "Content"})
    fetched = repo.get_by_id(db_session, created.id)

    assert fetched.id == created.id
    assert fetched.title == "Post"


def test_get_all_blog_posts(db_session):
    repo = BlogPostRepository()
    repo.create(db_session, {"title": "First", "content": "One"})
    repo.create(db_session, {"title": "Second", "content": "Two"})

    posts = repo.get_all(db_session)
    assert len(posts) >= 2
