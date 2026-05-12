from sqlalchemy.orm import Session

from app.models import (
    PostVote,
    CommentVote,
)


class VoteRepository:

    def get_post_vote(
        self,
        db: Session,
        post_u_id,
        user_u_id,
    ):
        return (
            db.query(PostVote)
            .filter(
                PostVote.post_u_id == post_u_id,
                PostVote.user_u_id == user_u_id,
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
        comment_u_id,
        user_u_id,
    ):
        return (
            db.query(CommentVote)
            .filter(
                CommentVote.comment_u_id == comment_u_id,
                CommentVote.user_u_id == user_u_id,
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