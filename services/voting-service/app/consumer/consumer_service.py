from uuid import UUID

from sqlalchemy.orm import Session

from app.queries.models import (
    PostVoteSummary,
    CommentVoteSummary,
    UserPostVote,
    UserCommentVote,
)


class ConsumerService:
    def apply_post_vote(
        self,
        db: Session,
        post_id: str,
        user_id: str,
        old_value: int,
        new_value: int,
    ):
        post_id = UUID(post_id)
        user_id = UUID(user_id)

        summary = db.get(PostVoteSummary, post_id)

        if not summary:
            summary = PostVoteSummary(
                post_id=post_id,
                upvotes=0,
                downvotes=0,
                score=0,
            )
            db.add(summary)

        existing_vote = (
            db.query(UserPostVote)
            .filter(
                UserPostVote.post_id == post_id,
                UserPostVote.user_id == user_id,
            )
            .first()
        )

        if not existing_vote:
            existing_vote = UserPostVote(
                post_id=post_id,
                user_id=user_id,
                value=0,
            )
            db.add(existing_vote)

        # remove old vote
        if old_value == 1:
            summary.upvotes -= 1
            summary.score -= 1

        elif old_value == -1:
            summary.downvotes -= 1
            summary.score += 1

        # apply new vote
        if new_value == 1:
            summary.upvotes += 1
            summary.score += 1

        elif new_value == -1:
            summary.downvotes += 1
            summary.score -= 1

        existing_vote.value = new_value

        db.commit()

    def apply_comment_vote(
        self,
        db: Session,
        comment_id: str,
        user_id: str,
        old_value: int,
        new_value: int,
    ):
        comment_id = UUID(comment_id)
        user_id = UUID(user_id)

        summary = db.get(CommentVoteSummary, comment_id)

        if not summary:
            summary = CommentVoteSummary(
                comment_id=comment_id,
                upvotes=0,
                downvotes=0,
                score=0,
            )
            db.add(summary)

        existing_vote = (
            db.query(UserCommentVote)
            .filter(
                UserCommentVote.comment_id == comment_id,
                UserCommentVote.user_id == user_id,
            )
            .first()
        )

        if not existing_vote:
            existing_vote = UserCommentVote(
                comment_id=comment_id,
                user_id=user_id,
                value=0,
            )
            db.add(existing_vote)

        # remove old vote
        if old_value == 1:
            summary.upvotes -= 1
            summary.score -= 1

        elif old_value == -1:
            summary.downvotes -= 1
            summary.score += 1

        # apply new vote
        if new_value == 1:
            summary.upvotes += 1
            summary.score += 1

        elif new_value == -1:
            summary.downvotes += 1
            summary.score -= 1

        existing_vote.value = new_value

        db.commit()
