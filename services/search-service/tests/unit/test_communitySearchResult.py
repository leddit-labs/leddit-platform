import pytest
from pydantic import ValidationError
from app.schemas import CommunitySearchResult


class TestCommunitySearchResultUId:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("u_id", [
        123,
        123.5,
    ])
    def test_invalid_u_id(self, u_id):
        with pytest.raises(ValidationError):
            CommunitySearchResult(u_id=u_id, name="Test Community")

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("u_id", [
        "Hello world",
        "456",
        "",
        " ",
        "A" * 1000,
    ])
    def test_valid_u_id(self, u_id):
        payload = CommunitySearchResult(u_id=u_id, name="Test Community")
        assert payload.u_id == u_id


class TestCommunitySearchResultName:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("name", [
        123,
        123.5,
    ])
    def test_invalid_name(self, name):
        with pytest.raises(ValidationError):
            CommunitySearchResult(u_id="community-123", name=name)

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("name", [
        "Hello world",
        "456",
        "",
        " ",
        "A" * 1000,
    ])
    def test_valid_name(self, name):
        payload = CommunitySearchResult(u_id="community-123", name=name)
        assert payload.name == name


class TestCommunitySearchResultDescription:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("description", [
        123,
        123.5,
    ])
    def test_invalid_description(self, description):
        with pytest.raises(ValidationError):
            CommunitySearchResult(u_id="community-123", name="Test Community", description=description)

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("description", [
        None,
        "Hello world",
        "456",
        "",
        " ",
        "A" * 1000,
    ])
    def test_valid_description(self, description):
        payload = CommunitySearchResult(u_id="community-123", name="Test Community", description=description)
        assert payload.description == description


class TestCommunitySearchResultCreatedBy:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("created_by", [
        123,
        123.5,
    ])
    def test_invalid_created_by(self, created_by):
        with pytest.raises(ValidationError):
            CommunitySearchResult(u_id="community-123", name="Test Community", created_by=created_by)

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("created_by", [
        None,
        "Hello world",
        "456",
        "",
        " ",
        "A" * 1000,
    ])
    def test_valid_created_by(self, created_by):
        payload = CommunitySearchResult(u_id="community-123", name="Test Community", created_by=created_by)
        assert payload.created_by == created_by


class TestCommunitySearchResultScore:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("score", [
        "not_a_number",
    ])
    def test_invalid_score(self, score):
        with pytest.raises(ValidationError):
            CommunitySearchResult(u_id="community-123", name="Test Community", score=score)

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("score", [
        None,
        0.5,
        123,           # int → coerced to float
        "123.45",      # string number → coerced to float
    ])
    def test_valid_score(self, score):
        payload = CommunitySearchResult(u_id="community-123", name="Test Community", score=score)
        if score is None:
            assert payload.score is None
        else:
            assert isinstance(payload.score, float)
            assert payload.score == float(score)