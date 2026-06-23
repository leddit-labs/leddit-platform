import pytest
from datetime import datetime
from pydantic import ValidationError
from app.schemas import UserProfile, UserUpdate


class TestUserProfileId:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("id_value", [
        123,
        123.45,
    ])
    def test_invalid_id(self, id_value):
        with pytest.raises(ValidationError):
            UserProfile(
                id=id_value,
                username="testuser",
                display_name=None,
                bio=None,
                avatar_url=None,
                post_karma=0,
                comment_karma=0,
                total_karma=0,
                created_at=datetime.now()
            )

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("id_value", [
        "Hello world",
        "456",
        "",
        " ",
        "A" * 1000,
    ])
    def test_valid_id(self, id_value):
        payload = UserProfile(
            id=id_value,
            username="testuser",
            display_name=None,
            bio=None,
            avatar_url=None,
            post_karma=0,
            comment_karma=0,
            total_karma=0,
            created_at=datetime.now()
        )
        assert payload.id == id_value


class TestUserProfileUsername:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("username", [
        123,
        123.45,
    ])
    def test_invalid_username(self, username):
        with pytest.raises(ValidationError):
            UserProfile(
                id="user-123",
                username=username,
                display_name=None,
                bio=None,
                avatar_url=None,
                post_karma=0,
                comment_karma=0,
                total_karma=0,
                created_at=datetime.now()
            )

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("username", [
        "Hello world",
        "456",
        "",
        " ",
        "A" * 1000,
    ])
    def test_valid_username(self, username):
        payload = UserProfile(
            id="user-123",
            username=username,
            display_name=None,
            bio=None,
            avatar_url=None,
            post_karma=0,
            comment_karma=0,
            total_karma=0,
            created_at=datetime.now()
        )
        assert payload.username == username


class TestUserProfileDisplayName:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("display_name", [
        123,
        123.45,
    ])
    def test_invalid_display_name(self, display_name):
        with pytest.raises(ValidationError):
            UserProfile(
                id="user-123",
                username="testuser",
                display_name=display_name,
                bio=None,
                avatar_url=None,
                post_karma=0,
                comment_karma=0,
                total_karma=0,
                created_at=datetime.now()
            )

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("display_name", [
        None,
        "Hello world",
        "456",
        "",
        " ",
        "A" * 1000,
    ])
    def test_valid_display_name(self, display_name):
        payload = UserProfile(
            id="user-123",
            username="testuser",
            display_name=display_name,
            bio=None,
            avatar_url=None,
            post_karma=0,
            comment_karma=0,
            total_karma=0,
            created_at=datetime.now()
        )
        assert payload.display_name == display_name


class TestUserProfileBio:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("bio", [
        123,
        123.45,
    ])
    def test_invalid_bio(self, bio):
        with pytest.raises(ValidationError):
            UserProfile(
                id="user-123",
                username="testuser",
                display_name=None,
                bio=bio,
                avatar_url=None,
                post_karma=0,
                comment_karma=0,
                total_karma=0,
                created_at=datetime.now()
            )

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("bio", [
        None,
        "Hello world",
        "456",
        "",
        " ",
        "A" * 1000,
    ])
    def test_valid_bio(self, bio):
        payload = UserProfile(
            id="user-123",
            username="testuser",
            display_name=None,
            bio=bio,
            avatar_url=None,
            post_karma=0,
            comment_karma=0,
            total_karma=0,
            created_at=datetime.now()
        )
        assert payload.bio == bio


class TestUserProfileAvatarUrl:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("avatar_url", [
        123,
        123.45,
    ])
    def test_invalid_avatar_url(self, avatar_url):
        with pytest.raises(ValidationError):
            UserProfile(
                id="user-123",
                username="testuser",
                display_name=None,
                bio=None,
                avatar_url=avatar_url,
                post_karma=0,
                comment_karma=0,
                total_karma=0,
                created_at=datetime.now()
            )

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("avatar_url", [
        None,
        "Hello world",
        "456",
        "",
        " ",
        "A" * 1000,
    ])
    def test_valid_avatar_url(self, avatar_url):
        payload = UserProfile(
            id="user-123",
            username="testuser",
            display_name=None,
            bio=None,
            avatar_url=avatar_url,
            post_karma=0,
            comment_karma=0,
            total_karma=0,
            created_at=datetime.now()
        )
        assert payload.avatar_url == avatar_url


class TestUserProfilePostKarma:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("post_karma", [
        "not_a_number",
        123.45,
        None,
    ])
    def test_invalid_post_karma(self, post_karma):
        with pytest.raises(ValidationError):
            UserProfile(
                id="user-123",
                username="testuser",
                display_name=None,
                bio=None,
                avatar_url=None,
                post_karma=post_karma,
                comment_karma=0,
                total_karma=0,
                created_at=datetime.now()
            )

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("post_karma", [
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
    def test_valid_post_karma(self, post_karma):
        payload = UserProfile(
            id="user-123",
            username="testuser",
            display_name=None,
            bio=None,
            avatar_url=None,
            post_karma=post_karma,
            comment_karma=0,
            total_karma=0,
            created_at=datetime.now()
        )
        assert payload.post_karma == post_karma


class TestUserProfileCommentKarma:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("comment_karma", [
        "not_a_number",
        123.45,
        None,
    ])
    def test_invalid_comment_karma(self, comment_karma):
        with pytest.raises(ValidationError):
            UserProfile(
                id="user-123",
                username="testuser",
                display_name=None,
                bio=None,
                avatar_url=None,
                post_karma=0,
                comment_karma=comment_karma,
                total_karma=0,
                created_at=datetime.now()
            )

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("comment_karma", [
        -999999,
        -1000
        -2,
        -1,
        0,
        1,
        2,
        1000,
        999999,
    ])
    def test_valid_comment_karma(self, comment_karma):
        payload = UserProfile(
            id="user-123",
            username="testuser",
            display_name=None,
            bio=None,
            avatar_url=None,
            post_karma=0,
            comment_karma=comment_karma,
            total_karma=0,
            created_at=datetime.now()
        )
        assert payload.comment_karma == comment_karma


class TestUserProfileTotalKarma:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("total_karma", [
        "not_a_number",
        123.45,
        None,
    ])
    def test_invalid_total_karma(self, total_karma):
        with pytest.raises(ValidationError):
            UserProfile(
                id="user-123",
                username="testuser",
                display_name=None,
                bio=None,
                avatar_url=None,
                post_karma=0,
                comment_karma=0,
                total_karma=total_karma,
                created_at=datetime.now()
            )

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("total_karma", [
        -999999,
        -1000
        -2,
        -1,
        0,
        1,
        2,
        1000,
        999999,
    ])
    def test_valid_total_karma(self, total_karma):
        payload = UserProfile(
            id="user-123",
            username="testuser",
            display_name=None,
            bio=None,
            avatar_url=None,
            post_karma=0,
            comment_karma=0,
            total_karma=total_karma,
            created_at=datetime.now()
        )
        assert payload.total_karma == total_karma


class TestUserProfileCreatedAt:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("created_at", [
        "not_a_datetime",
        None,
    ])
    def test_invalid_created_at(self, created_at):
        with pytest.raises(ValidationError):
            UserProfile(
                id="user-123",
                username="testuser",
                display_name=None,
                bio=None,
                avatar_url=None,
                post_karma=0,
                comment_karma=0,
                total_karma=0,
                created_at=created_at
            )

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("created_at", [
        datetime(2024, 1, 1, 12, 0, 0),      # 1. Native datetime
        1704067200,                          # 2. Numeric timestamp (int)
        "2024-01-01T12:00:00",               # 3. ISO format string
    ])
    def test_valid_created_at(self, created_at):
        payload = UserProfile(
            id="user-123",
            username="testuser",
            display_name=None,
            bio=None,
            avatar_url=None,
            post_karma=0,
            comment_karma=0,
            total_karma=0,
            created_at=created_at
        )
        assert isinstance(payload.created_at, datetime)

class TestUserUpdateDisplayName:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("display_name", [
        123,
        123.45,
    ])
    def test_invalid_display_name(self, display_name):
        with pytest.raises(ValidationError):
            UserUpdate(display_name=display_name)

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("display_name", [
        None,
        "Hello world",
        "456",
        "",
        " ",
        "A" * 1000,
    ])
    def test_valid_display_name(self, display_name):
        payload = UserUpdate(display_name=display_name)
        assert payload.display_name == display_name


class TestUserUpdateBio:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("bio", [
        123,
        123.45,
    ])
    def test_invalid_bio(self, bio):
        with pytest.raises(ValidationError):
            UserUpdate(bio=bio)

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("bio", [
        None,
        "Hello world",
        "456",
        "",
        " ",
        "A" * 1000,
    ])
    def test_valid_bio(self, bio):
        payload = UserUpdate(bio=bio)
        assert payload.bio == bio


class TestUserUpdateAvatarUrl:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("avatar_url", [
        123,
        123.45,
    ])
    def test_invalid_avatar_url(self, avatar_url):
        with pytest.raises(ValidationError):
            UserUpdate(avatar_url=avatar_url)

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("avatar_url", [
        None,
        "Hello world",
        "456",
        "",
        " ",
        "A" * 1000,
    ])
    def test_valid_avatar_url(self, avatar_url):
        payload = UserUpdate(avatar_url=avatar_url)
        assert payload.avatar_url == avatar_url


class TestUserUpdateEmpty:
    # -------------------- VALID VALUES --------------------
    def test_empty_update_valid(self):
        # UserUpdate() with no fields is valid.
        payload = UserUpdate()
        assert payload.display_name is None
        assert payload.bio is None
        assert payload.avatar_url is None