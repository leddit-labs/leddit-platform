import pytest
from pydantic import ValidationError
from app.queries.schemas import UserVoteOut


class TestUserVoteOutValue:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("value", [
        "not_a_number",
        123.45,
        None,
    ])
    def test_invalid_value(self, value):
        with pytest.raises(ValidationError):
            UserVoteOut(value=value)

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("value", [
        -999999,
        -1000,
        -2,
        -1,
        0,
        1,
        2,
        1000,
        999999,
    ])
    def test_valid_value(self, value):
        payload = UserVoteOut(value=value)
        if isinstance(value, str):
            assert payload.value == int(value)
        else:
            assert payload.value == value