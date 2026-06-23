import pytest
from uuid import UUID, uuid4
from pydantic import ValidationError
from app.commands.schemas import VoteCreate


class TestVoteCreateUserId:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("user_id", [
        "not-a-uuid",
        "123",
        None,
    ])
    def test_invalid_user_id(self, user_id):
        with pytest.raises(ValidationError):
            VoteCreate(
                user_id=user_id,
                value=1
            )

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("user_id", [
        uuid4(),
        str(uuid4()),
    ])
    def test_valid_user_id(self, user_id):
        payload = VoteCreate(
            user_id=user_id,
            value=1
        )
        assert isinstance(payload.user_id, UUID)


class TestVoteCreateValue:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("value", [
        -10,
        -5,
        -3,
        -2,
        0,
        2,
        3,
        5,
        10,
        "not_a_number",
        123.45,
    ])
    def test_invalid_value(self, value):
        with pytest.raises(ValidationError):
            VoteCreate(
                user_id=uuid4(),
                value=value
            )

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("value", [
        -1,   # Downvote
        1,    # Upvote
    ])
    def test_valid_value(self, value):
        payload = VoteCreate(
            user_id=uuid4(),
            value=value
        )
        assert payload.value == value

    # -------------------- VALIDATOR ERROR MESSAGE --------------------
    def test_value_validator_error_message(self):
        with pytest.raises(ValidationError) as exc_info:
            VoteCreate(
                user_id=uuid4(),
                value=0
            )
        assert "Vote value must be -1 or 1" in str(exc_info.value)