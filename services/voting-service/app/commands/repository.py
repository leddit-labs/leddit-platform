from sqlalchemy.orm import Session

from app.commands.models import (
    PostVote,
    CommentVote,
)


class VoteRepository:

    def get_post_vote(
        self,
        db: Session,
        post_id,
        user_id,
    ):
        return (
            db.query(PostVote)
            .filter(
                PostVote.post_id == post_id,
                PostVote.user_id == user_id,
            )
            .first()
        )

    def create_post_vote(
        self,
        db: Session,
        vote: PostVote,
    ):
        db.add(vote)

        db.commit()
        db.refresh(vote)

        return vote

    def get_comment_vote(
        self,
        db: Session,
        comment_id,
        user_id,
    ):
        return (
            db.query(CommentVote)
            .filter(
                CommentVote.comment_id == comment_id,
                CommentVote.user_id == user_id,
            )
            .first()
        )

    def create_comment_vote(
        self,
        db: Session,
        vote: CommentVote,
    ):
        db.add(vote)

        db.commit()
        db.refresh(vote)

        return vote

    def update_vote(
        self,
        db: Session,
        vote,
        value: int,
    ):
        vote.value = value

        db.commit()
        db.refresh(vote)

        return vote

    #probably don't need a delete
    """
    def delete_vote(
        self,
        db: Session,
        vote,
    ):
        db.delete(vote)

        db.commit()
    """