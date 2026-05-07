import pytest
from pydantic import ValidationError

from app.schemas import CommentCreate, CommentUpdate


class TestCommentCreatePostId:
    @pytest.mark.parametrize(
        "post_id",
        [
            "",
            "A" * 65,
            "A" * 66,
            "A" * 100,
            123,
        ],
    )
    def test_invalid_post_id(self, post_id):
        with pytest.raises(ValidationError):
            CommentCreate(post_id=post_id, parent_id=None, author_id="author-1", content="hello")

    @pytest.mark.parametrize(
        "post_id",
        [
            "A",
            "A" * 2,
            "A" * 35,
            "A" * 63,
            "A" * 64,
        ],
    )
    def test_valid_post_id(self, post_id):
        payload = CommentCreate(post_id=post_id, parent_id=None, author_id="author-1", content="hello")

        assert payload.post_id == post_id


class TestCommentCreateAuthorId:
    @pytest.mark.parametrize(
        "author_id",
        [
            "",
            "A" * 65,
            "A" * 66,
            "A" * 100,
            123,
        ],
    )
    def test_invalid_author_id(self, author_id):
        with pytest.raises(ValidationError):
            CommentCreate(post_id="post-1", parent_id=None, author_id=author_id, content="hello")

    @pytest.mark.parametrize(
        "author_id",
        [
            "A",
            "A" * 2,
            "A" * 35,
            "A" * 63,
            "A" * 64,
        ],
    )
    def test_valid_author_id(self, author_id):
        payload = CommentCreate(post_id="post-1", parent_id=None, author_id=author_id, content="hello")

        assert payload.author_id == author_id


class TestCommentCreateContent:
    @pytest.mark.parametrize(
        "content",
        [
            "",
            "A" * 5001,
            "A" * 7500,
            123,
        ],
    )
    def test_invalid_content(self, content):
        with pytest.raises(ValidationError):
            CommentCreate(post_id="post-1", parent_id=None, author_id="author-1", content=content)

    @pytest.mark.parametrize(
        "content",
        [
            "A",
            "A" * 2,
            "A" * 2500,
            "A" * 4999,
            "A" * 5000,
        ],
    )
    def test_valid_content(self, content):
        payload = CommentCreate(post_id="post-1", parent_id=None, author_id="author-1", content=content)

        assert payload.content == content


class TestCommentUpdateContent:
    @pytest.mark.parametrize(
        "content",
        [
            "",
            "A" * 5001,
            "A" * 7500,
            123,
        ],
    )
    def test_comment_update_rejects_invalid_content(self, content):
        with pytest.raises(ValidationError):
            CommentUpdate(content=content)

    @pytest.mark.parametrize(
        "content",
        [
            "A",
            "A" * 2,
            "A" * 2500,
            "A" * 4999,
            "A" * 5000,
        ],
    )
    def test_comment_update_accepts_valid_content(self, content):
        payload = CommentUpdate(content=content)

        assert payload.content == content