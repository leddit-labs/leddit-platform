import pytest
from pydantic import ValidationError

from app.schemas import RuleIn, RuleUpdate

class TestRuleInTitle:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("title", [
        "",
        "A" * 101,
        "A" * 102,
        "A" * 200,
        None,
        123,
    ])
    def test_invalid_title(self, title):
        with pytest.raises(ValidationError):
            RuleIn(title=title, text="test text")

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("title", [
        "A",
        "AB",
        "A" * 50,
        "A" * 99,
        "A" * 100,
        "Hello World",
        "hello-world",
        "hello_world",
        "123",
        "Über",
        "name!",
    ])
    def test_valid_title(self, title):
        payload = RuleIn(title=title, text="test text")
        assert payload.title == title


class TestRuleInText:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("text", [
        "",
        "A" * 501,
        "A" * 502,
        "A" * 1000,
        None,
        123,
    ])
    def test_invalid_text(self, text):
        with pytest.raises(ValidationError):
            RuleIn(title="testTitle", text=text)

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("text", [
        "A",
        "AB",
        "A" * 250,
        "A" * 499,
        "A" * 500,
        "This is a full sentence.",
        "123-456",
        "Über",
    ])
    def test_valid_text(self, text):
        payload = RuleIn(title="testTitle", text=text)
        assert payload.text == text


class TestRuleUpdateTitle:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("title", [
        "",
        "A" * 101,
        "A" * 102,
        "A" * 200,
        123,
    ])
    def test_invalid_title(self, title):
        with pytest.raises(ValidationError):
            RuleUpdate(title=title)

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("title", [
        None,
        "A",
        "AB",
        "A" * 50,
        "A" * 99,
        "A" * 100,
        "Hello World",
        "hello_world",
        "Über",
    ])
    def test_valid_title(self, title):
        payload = RuleUpdate(title=title)
        assert payload.title == title

    def test_update_with_no_fields(self):
        payload = RuleUpdate()
        assert payload.title is None
        assert payload.text is None


class TestRuleUpdateText:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("text", [
        "",
        "A" * 501,
        "A" * 502,
        "A" * 1000,
        123,
    ])
    def test_invalid_text(self, text):
        with pytest.raises(ValidationError):
            RuleUpdate(text=text)

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("text", [
        None,
        "A",
        "AB",
        "A" * 250,
        "A" * 499,
        "A" * 500,
        "This is a full sentence.",
    ])
    def test_valid_text(self, text):
        payload = RuleUpdate(text=text)
        assert payload.text == text

    def test_update_with_text_none(self):
        payload = RuleUpdate(text=None)
        assert payload.text is None