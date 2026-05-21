from uuid import UUID

from sqlalchemy.orm import Session

from app.queries.models import (
    PostVoteSummary,
    CommentVoteSummary,
    UserPostVote,
    UserCommentVote,
)


class ConsumerService:
    # a vote has been made on a post, now the summaries should be updated
    def apply_post_vote(
        self,
        db: Session,
        post_id: str,
        user_id: str,
        new_value: int,
    ):
        #convert from raw str to ensure correct UUID type.
        post_id = UUID(post_id)
        user_id = UUID(user_id)

        # ensure summary exists
        summary = db.get(PostVoteSummary, post_id)
        if not summary:
            summary = PostVoteSummary(
                post_id=post_id,
                upvotes=0,
                downvotes=0,
                score=0,
            )
            db.add(summary)

        # get current stored user vote (source of truth)
        vote = (
            db.query(UserPostVote)
            .filter(
                UserPostVote.post_id == post_id,
                UserPostVote.user_id == user_id,
            )
            .first()
        )

        old_value = vote.value if vote else 0

        # idempotency check (duplicate event) return if this is a duplicate
        if old_value == new_value:
            db.commit()
            return

        delta = new_value - old_value

        # if vote does not exist, make a new one
        if not vote:
            vote = UserPostVote(
                post_id=post_id,
                user_id=user_id,
                value=new_value,
            )
            db.add(vote)
        else:
            vote.value = new_value

        # apply summary changes
        summary.score += delta

        if old_value == 1:
            summary.upvotes -= 1
        elif old_value == -1:
            summary.downvotes -= 1

        if new_value == 1:
            summary.upvotes += 1
        elif new_value == -1:
            summary.downvotes += 1

        db.commit()

    # a vote has been made on a comment, now the summaries should be updated
    def apply_comment_vote(
        self,
        db: Session,
        comment_id: str,
        user_id: str,
        new_value: int,
    ):
        #convert from raw str to ensure correct UUID type.
        comment_id = UUID(comment_id)
        user_id = UUID(user_id)

        #ensure summary exists
        summary = db.get(CommentVoteSummary, comment_id)
        if not summary:
            summary = CommentVoteSummary(
                comment_id=comment_id,
                upvotes=0,
                downvotes=0,
                score=0,
            )
            db.add(summary)

        # get current stored user vote (source of truth)
        vote = (
            db.query(UserCommentVote)
            .filter(
                UserCommentVote.comment_id == comment_id,
                UserCommentVote.user_id == user_id,
            )
            .first()
        )

        old_value = vote.value if vote else 0

        # idempotency check (duplicate event) return if this is a duplicate
        if old_value == new_value:
            db.commit()
            return

        delta = new_value - old_value

        # if vote does not exist, make a new one
        if not vote:
            vote = UserCommentVote(
                comment_id=comment_id,
                user_id=user_id,
                value=new_value,
            )
            db.add(vote)
        else:
            vote.value = new_value

        # apply summary changes
        summary.score += delta

        if old_value == 1:
            summary.upvotes -= 1
        elif old_value == -1:
            summary.downvotes -= 1

        if new_value == 1:
            summary.upvotes += 1
        elif new_value == -1:
            summary.downvotes += 1

        db.commit()
