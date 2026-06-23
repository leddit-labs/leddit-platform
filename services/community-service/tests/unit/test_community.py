import pytest
from pydantic import ValidationError

from app.schemas import CommunityCreate

class TestCommunityCreateName:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("name", [
        "",
        "A",
        "AB",
        "A" * 51,
        "A" * 52,
        "A" * 100,
        123,
        None,
        "name with space",
        "hello-world",
        "hello@world",
        "hello.world",
        "123-abc",
        "Über",
        "привет",
        "name!",
        "name#",
    ])
    def test_invalid_name(self, name):
        with pytest.raises(ValidationError):
            CommunityCreate(name=name, description="testDescription", owner_id="user-1")

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("name", [
        "ABC",
        "ABCD",
        "A" * 25,
        "A" * 49,
        "A" * 50,
        "abc",
        "123",
        "hello_world",
    ])
    def test_valid_name(self, name):
        payload = CommunityCreate(name=name, description="testDescription", owner_id="user-1")
        assert payload.name == name


class TestCommunityCreateDescription:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("description", [
        "A" * 501,
        "A" * 502,
        "A" * 1000,       
        None,
        123,
    ])
    def test_invalid_description(self, description):
        with pytest.raises(ValidationError):
            CommunityCreate(name="testName", owner_id="user-1", description=description)

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("description", [
        "",
        "A",
        "AB",
        "A" * 250,
        "A" * 499,
        "A" * 500,
        "Hello World",
        "hello-world",
        "hello@world",
        "hello.world",
        "Über",
        "привет",
    ])
    def test_valid_description(self, description):
        payload = CommunityCreate(name="testName", owner_id="user-1", description=description)
        assert payload.description == description