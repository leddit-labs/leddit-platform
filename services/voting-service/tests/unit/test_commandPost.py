import pytest
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import ValidationError
from app.commands.schemas import PostVoteOut


class TestPostVoteOutUId:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("u_id", [
        "not-a-uuid",
        "123",
        None,
    ])
    def test_invalid_u_id(self, u_id):
        with pytest.raises(ValidationError):
            PostVoteOut(
                u_id=u_id,
                post_id=uuid4(),
                user_id=uuid4(),
                value=1,
                created_at=datetime.now()
            )

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("u_id", [
        uuid4(),
        str(uuid4()),
    ])
    def test_valid_u_id(self, u_id):
        payload = PostVoteOut(
            u_id=u_id,
            post_id=uuid4(),
            user_id=uuid4(),
            value=1,
            created_at=datetime.now()
        )
        assert isinstance(payload.u_id, UUID)


class TestPostVoteOutPostId:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("post_id", [
        "not-a-uuid",
        "123",
        None,
    ])
    def test_invalid_post_id(self, post_id):
        with pytest.raises(ValidationError):
            PostVoteOut(
                u_id=uuid4(),
                post_id=post_id,
                user_id=uuid4(),
                value=1,
                created_at=datetime.now()
            )

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("post_id", [
        uuid4(),
        str(uuid4()),
    ])
    def test_valid_post_id(self, post_id):
        payload = PostVoteOut(
            u_id=uuid4(),
            post_id=post_id,
            user_id=uuid4(),
            value=1,
            created_at=datetime.now()
        )
        assert isinstance(payload.post_id, UUID)


class TestPostVoteOutUserId:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("user_id", [
        "not-a-uuid",
        "123",
        None,
    ])
    def test_invalid_user_id(self, user_id):
        with pytest.raises(ValidationError):
            PostVoteOut(
                u_id=uuid4(),
                post_id=uuid4(),
                user_id=user_id,
                value=1,
                created_at=datetime.now()
            )

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("user_id", [
        uuid4(),
        str(uuid4()),
    ])
    def test_valid_user_id(self, user_id):
        payload = PostVoteOut(
            u_id=uuid4(),
            post_id=uuid4(),
            user_id=user_id,
            value=1,
            created_at=datetime.now()
        )
        assert isinstance(payload.user_id, UUID)


class TestPostVoteOutValue:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("value", [
        "not_a_number",
        123.45,
        None,
    ])
    def test_invalid_value(self, value):
        with pytest.raises(ValidationError):
            PostVoteOut(
                u_id=uuid4(),
                post_id=uuid4(),
                user_id=uuid4(),
                value=value,
                created_at=datetime.now()
            )

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
        payload = PostVoteOut(
            u_id=uuid4(),
            post_id=uuid4(),
            user_id=uuid4(),
            value=value,
            created_at=datetime.now()
        )
        assert payload.value == value


class TestPostVoteOutCreatedAt:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("created_at", [
        "not_a_datetime",
        None,
    ])
    def test_invalid_created_at(self, created_at):
        with pytest.raises(ValidationError):
            PostVoteOut(
                u_id=uuid4(),
                post_id=uuid4(),
                user_id=uuid4(),
                value=1,
                created_at=created_at
            )

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("created_at", [
        datetime(2024, 1, 1, 12, 0, 0),      # 1. Native datetime
        1704067200,                          # 2. Numeric timestamp (int)
        "2024-01-01T12:00:00",               # 3. ISO format string
    ])
    def test_valid_created_at(self, created_at):
        payload = PostVoteOut(
            u_id=uuid4(),
            post_id=uuid4(),
            user_id=uuid4(),
            value=1,
            created_at=created_at
        )
        assert isinstance(payload.created_at, datetime)