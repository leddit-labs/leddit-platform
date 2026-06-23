import pytest
from pydantic import ValidationError
from app.schemas import PostSearchResult


class TestPostSearchResultUId:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("u_id", [
        123,
        123.5,
    ])
    def test_invalid_u_id(self, u_id):
        with pytest.raises(ValidationError):
            PostSearchResult(u_id=u_id, title="Test Post")

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("u_id", [
        "Hello world",
        "456",
        "",
        " ",
        "A" * 1000,
    ])
    def test_valid_u_id(self, u_id):
        payload = PostSearchResult(u_id=u_id, title="Test Post")
        assert payload.u_id == u_id


class TestPostSearchResultTitle:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("title", [
        123,
        123.5,
    ])
    def test_invalid_title(self, title):
        with pytest.raises(ValidationError):
            PostSearchResult(u_id="post-123", title=title)

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("title", [
        "Hello world",
        "456",
        "",
        " ",
        "A" * 1000,
    ])
    def test_valid_title(self, title):
        payload = PostSearchResult(u_id="post-123", title=title)
        assert payload.title == title


class TestPostSearchResultCommunityId:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("community_id", [
        123,
        123.5,
    ])
    def test_invalid_community_id(self, community_id):
        with pytest.raises(ValidationError):
            PostSearchResult(u_id="post-123", title="Test Post", community_id=community_id)

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("community_id", [
        None,
        "Hello world",
        "456",
        "",
        " ",
        "A" * 1000,
    ])
    def test_valid_community_id(self, community_id):
        payload = PostSearchResult(u_id="post-123", title="Test Post", community_id=community_id)
        assert payload.community_id == community_id


class TestPostSearchResultAuthorId:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("author_id", [
        123,
        123.5,
    ])
    def test_invalid_author_id(self, author_id):
        with pytest.raises(ValidationError):
            PostSearchResult(u_id="post-123", title="Test Post", author_id=author_id)

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("author_id", [
        None,
        "Hello world",
        "456",
        "",
        " ",
        "A" * 1000,
    ])
    def test_valid_author_id(self, author_id):
        payload = PostSearchResult(u_id="post-123", title="Test Post", author_id=author_id)
        assert payload.author_id == author_id


class TestPostSearchResultContent:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("content", [
        123,
        123.5,
    ])
    def test_invalid_content(self, content):
        with pytest.raises(ValidationError):
            PostSearchResult(u_id="post-123", title="Test Post", content=content)

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
        payload = PostSearchResult(u_id="post-123", title="Test Post", content=content)
        assert payload.content == content


class TestPostSearchResultScore:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("score", [
        "not_a_number",
    ])
    def test_invalid_score(self, score):
        with pytest.raises(ValidationError):
            PostSearchResult(u_id="post-123", title="Test Post", score=score)

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("score", [
        None,
        0.5,
        123,           # int → coerced to float
        "123.45",      # string number → coerced to float
    ])
    def test_valid_score(self, score):
        payload = PostSearchResult(u_id="post-123", title="Test Post", score=score)
        if score is None:
            assert payload.score is None
        else:
            assert isinstance(payload.score, float)
            assert payload.score == float(score)