import pytest
from uuid import UUID, uuid4
from pydantic import ValidationError
from app.queries.schemas import CommentVoteSummaryOut


class TestCommentVoteSummaryOutCommentId:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("comment_id", [
        "not-a-uuid",
        "123",
        None,
    ])
    def test_invalid_comment_id(self, comment_id):
        with pytest.raises(ValidationError):
            CommentVoteSummaryOut(
                comment_id=comment_id,
                upvotes=0,
                downvotes=0,
                score=0
            )

    # -------------------- VALID VALUES --------------------
    @pytest.mark.parametrize("comment_id", [
        uuid4(),
        str(uuid4()),
    ])
    def test_valid_comment_id(self, comment_id):
        payload = CommentVoteSummaryOut(
            comment_id=comment_id,
            upvotes=0,
            downvotes=0,
            score=0
        )
        assert isinstance(payload.comment_id, UUID)


class TestCommentVoteSummaryOutUpvotes:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("upvotes", [
        "not_a_number",
        123.45,
        None,
    ])
    def test_invalid_upvotes(self, upvotes):
        with pytest.raises(ValidationError):
            CommentVoteSummaryOut(
                comment_id=uuid4(),
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
        payload = CommentVoteSummaryOut(
            comment_id=uuid4(),
            upvotes=upvotes,
            downvotes=0,
            score=0
        )
        assert payload.upvotes == upvotes


class TestCommentVoteSummaryOutDownvotes:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("downvotes", [
        "not_a_number",
        123.45,
        None,
    ])
    def test_invalid_downvotes(self, downvotes):
        with pytest.raises(ValidationError):
            CommentVoteSummaryOut(
                comment_id=uuid4(),
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
        payload = CommentVoteSummaryOut(
            comment_id=uuid4(),
            upvotes=0,
            downvotes=downvotes,
            score=0
        )
        assert payload.downvotes == downvotes


class TestCommentVoteSummaryOutScore:
    # -------------------- INVALID VALUES --------------------
    @pytest.mark.parametrize("score", [
        "not_a_number",
        123.45,
        None,
    ])
    def test_invalid_score(self, score):
        with pytest.raises(ValidationError):
            CommentVoteSummaryOut(
                comment_id=uuid4(),
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
        payload = CommentVoteSummaryOut(
            comment_id=uuid4(),
            upvotes=0,
            downvotes=0,
            score=score
        )
        assert payload.score == score