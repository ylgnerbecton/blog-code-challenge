from src.domain.entities.blog_post import BlogPostEntity
from src.domain.entities.comment import CommentEntity


def test_blog_post_entity_creation_with_comments():
    comment = CommentEntity(id=1, post_id=10, content="First comment")
    post = BlogPostEntity(
        id=10, title="My Blog Post", content="This is the content", comments=[comment]
    )

    assert post.id == 10
    assert post.title == "My Blog Post"
    assert post.content == "This is the content"
    assert len(post.comments) == 1
    assert post.comments[0].content == "First comment"
    assert post.comments[0].post_id == 10


def test_blog_post_entity_empty_comments():
    post = BlogPostEntity(
        id=11, title="Post without comments", content="Still a valid post", comments=[]
    )

    assert post.comments == []
    assert post.title == "Post without comments"
