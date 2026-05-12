from sqlalchemy.orm import Session

from app.vote_repository import VoteRepository

from app.models import (
    PostVote,
    CommentVote,
)

from app.schemas import VoteCreate

# TODO
# from app.messaging import publish_event


class VoteService:
    def __init__(self):
        self.repo = VoteRepository()

    # POSTS

    def vote_post(
        self,
        db: Session,
        post_u_id,
        data: VoteCreate,
    ) -> PostVote:
        # logic below is for making this an Idepempotent Operation
        # if users new voting requst matches an existing vote. return the existing vote
        existing_vote = self.repo.get_post_vote(
            db,
            post_u_id,
            data.user_id,
        )

        old_value = 0

        if existing_vote:
            if existing_vote.value == data.value:
                return existing_vote

            old_value = existing_vote.value

            vote = self.repo.update_vote(
                db,
                existing_vote,
                data.value,
            )

        else:
            vote = PostVote(
                post_u_id=post_u_id,
                user_u_id=data.user_u_id,
                value=data.value,
            )

            vote = self.repo.create_post_vote(
                db,
                vote,
            )

        # below is to tell the future voting read model to update
        """
        publish_event(
            "vote.post.changed",
            {
                "post_u_id": str(post_u_id),
                "user_u_id": str(data.user_u_id),
                "old_value": old_value,
                "new_value": data.value,
            },
        )
        """

        return vote

    # COMMENTS

    def vote_comment(
        self,
        db: Session,
        comment_u_id,
        data: VoteCreate,
    ):
        existing_vote = self.repo.get_comment_vote(
            db,
            comment_u_id,
            data.user_u_id,
        )

        old_value = 0

        if existing_vote:
            if existing_vote.value == data.value:
                return existing_vote

            old_value = existing_vote.value

            vote = self.repo.update_vote(
                db,
                existing_vote,
                data.value,
            )

        else:
            vote = CommentVote(
                comment_u_id=comment_u_id,
                user_u_id=data.user_id,
                value=data.value,
            )

            vote = self.repo.create_comment_vote(
                db,
                vote,
            )

        """
        publish_event(
            "vote.comment.changed",
            {
                "comment_u_id": str(comment_u_id),
                "user_u_id": str(data.user_u_id),
                "old_value": old_value,
                "new_value": data.value,
            },
        )
        """

        return vote
