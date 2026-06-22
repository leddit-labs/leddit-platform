import pytest
from uuid import UUID, uuid4
from pydantic import ValidationError
from app.schemas import PostCreate, PostUpdate


class TestPostCreateCommunityId:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("community_id", [
        "not-a-uuid",
        "123",
    ])
    def test_invalid_community_id(self, community_id):
        with pytest.raises(ValidationError):
            PostCreate(
                community_id=community_id,
                author_id=uuid4(),
                title="Valid Title"
            )

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("community_id", [
        uuid4(),
        str(uuid4()),
    ])
    def test_valid_community_id(self, community_id):
        payload = PostCreate(
            community_id=community_id,
            author_id=uuid4(),
            title="Valid Title"
        )
        assert isinstance(payload.community_id, UUID)


class TestPostCreateAuthorId:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("author_id", [
        "not-a-uuid",
        "123",
    ])
    def test_invalid_author_id(self, author_id):
        with pytest.raises(ValidationError):
            PostCreate(
                community_id=uuid4(),
                author_id=author_id,
                title="Valid Title"
            )

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("author_id", [
        uuid4(),
        str(uuid4()),
    ])
    def test_valid_author_id(self, author_id):
        payload = PostCreate(
            community_id=uuid4(),
            author_id=author_id,
            title="Valid Title"
        )
        assert isinstance(payload.author_id, UUID)


class TestPostCreateTitle:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("title", [
        123,
        None,
    ])
    def test_invalid_title(self, title):
        with pytest.raises(ValidationError):
            PostCreate(
                community_id=uuid4(),
                author_id=uuid4(),
                title=title
            )

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("title", [
        "",
        "A",
        "AB",
        "A" * 1000,
        "Hello World",
        "123",
    ])
    def test_valid_title_strings(self, title):
        payload = PostCreate(
            community_id=uuid4(),
            author_id=uuid4(),
            title=title
        )
        assert payload.title == title


class TestPostCreateContent:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("content", [
        123,
        3.14,
    ])
    def test_invalid_content_values(self, content):
        with pytest.raises(ValidationError):
            PostCreate(
                community_id=uuid4(),
                author_id=uuid4(),
                title="Title",
                content=content
            )
            
    # -------------------- VALID VALUES --------------------
    def test_content_defaults_to_none(self):
        #When 'content' is omitted, it should default to None.
        payload = PostCreate(
            community_id=uuid4(),
            author_id=uuid4(),
            title="Title"
        )
        assert payload.content is None

    @pytest.mark.parametrize("content", [
        None,               # None (same result as omission)
        "",
        " ",
        "Hello World",
        "hello-world",
        "hello@world",
        "hello.world",
        "Über",
        "привет",
    ])
    def test_valid_content_values(self, content):
        payload = PostCreate(
            community_id=uuid4(),
            author_id=uuid4(),
            title="Title",
            content=content
        )
        assert payload.content == content


class TestPostUpdateTitle:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("title", [
        123,
        3.14,
    ])
    def test_invalid_title(self, title):
        with pytest.raises(ValidationError):
            PostUpdate(title=title)

    # -------------------- VALID VALUES --------------------
    def test_empty_update_valid(self):
        # PostUpdate() with no fields is valid.
        payload = PostUpdate()
        assert payload.title is None
        assert payload.content is None

    @pytest.mark.parametrize("title", [
        None,
        "Hello world",
        "123",
        "",
        " ",
        "A" * 1000,
    ])
    def test_valid_title(self, title):
        payload = PostUpdate(title=title)
        assert payload.title == title


class TestPostUpdateContent:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("content", [
        123,
        3.14,
    ])
    def test_invalid_content(self, content):
        with pytest.raises(ValidationError):
            PostUpdate(content=content)

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("content", [
        None,
        "Hello world",
        "456",
        "",
        " ",
        "A" * 1000,
    ])
    def test_valid_content(self, content):
        payload = PostUpdate(content=content)
        assert payload.content == content