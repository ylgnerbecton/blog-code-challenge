from src.domain.entities.comment import CommentEntity


def test_comment_entity_creation():
    comment = CommentEntity(id=1, post_id=10, content="Nice article!")

    assert comment.id == 1
    assert comment.content == "Nice article!"
    assert comment.post_id == 10


def test_comment_entity_str_representation():
    comment = CommentEntity(id=42, post_id=99, content="Interesting point")
    assert comment.id == 42
    assert comment.post_id == 99
    assert comment.content == "Interesting point"
