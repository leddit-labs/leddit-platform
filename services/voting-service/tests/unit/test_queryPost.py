import pytest
from uuid import UUID, uuid4
from pydantic import ValidationError
from app.queries.schemas import PostVoteSummaryOut


class TestPostVoteSummaryOutPostId:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("post_id", [
        "not-a-uuid",
        "123",
        None,
    ])
    def test_invalid_post_id(self, post_id):
        with pytest.raises(ValidationError):
            PostVoteSummaryOut(
                post_id=post_id,
                upvotes=0,
                downvotes=0,
                score=0
            )

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("post_id", [
        uuid4(),
        str(uuid4()),
    ])
    def test_valid_post_id(self, post_id):
        payload = PostVoteSummaryOut(
            post_id=post_id,
            upvotes=0,
            downvotes=0,
            score=0
        )
        assert isinstance(payload.post_id, UUID)


class TestPostVoteSummaryOutUpvotes:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("upvotes", [
        "not_a_number",
        123.45,
        None,
    ])
    def test_invalid_upvotes(self, upvotes):
        with pytest.raises(ValidationError):
            PostVoteSummaryOut(
                post_id=uuid4(),
                upvotes=upvotes,
                downvotes=0,
                score=0
            )

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("upvotes", [
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
    def test_valid_upvotes(self, upvotes):
        payload = PostVoteSummaryOut(
            post_id=uuid4(),
            upvotes=upvotes,
            downvotes=0,
            score=0
        )
        assert payload.upvotes == upvotes


class TestPostVoteSummaryOutDownvotes:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("downvotes", [
        "not_a_number",
        123.45,
        None,
    ])
    def test_invalid_downvotes(self, downvotes):
        with pytest.raises(ValidationError):
            PostVoteSummaryOut(
                post_id=uuid4(),
                upvotes=0,
                downvotes=downvotes,
                score=0
            )

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("downvotes", [
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
    def test_valid_downvotes(self, downvotes):
        payload = PostVoteSummaryOut(
            post_id=uuid4(),
            upvotes=0,
            downvotes=downvotes,
            score=0
        )
        if isinstance(downvotes, str):
            assert payload.downvotes == int(downvotes)
        else:
            assert payload.downvotes == downvotes


class TestPostVoteSummaryOutScore:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("score", [
        "not_a_number",
        123.45,
        None,
    ])
    def test_invalid_score(self, score):
        with pytest.raises(ValidationError):
            PostVoteSummaryOut(
                post_id=uuid4(),
                upvotes=0,
                downvotes=0,
                score=score
            )

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("score", [
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
    def test_valid_score(self, score):
        payload = PostVoteSummaryOut(
            post_id=uuid4(),
            upvotes=0,
            downvotes=0,
            score=score
        )
        if isinstance(score, str):
            assert payload.score == int(score)
        else:
            assert payload.score == score