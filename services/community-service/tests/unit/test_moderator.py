import pytest
from pydantic import ValidationError

from app.schemas import ModeratorAdd

class TestModeratorAddUserId:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("user_id", [
        "",
        None,
        123,
    ])
    def test_invalid_user_id(self, user_id):
        with pytest.raises(ValidationError):
            ModeratorAdd(user_id=user_id)

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("user_id", [
        "a",
        "ab",
        "a" * 250,
        "a" * 1000,
        " ",
        "user-123",
        "user_123",
        "user@example",
        "user with space",
        "Üser",
    ])
    def test_valid_user_id(self, user_id):
        payload = ModeratorAdd(user_id=user_id)
        assert payload.user_id == user_id