from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.vote_service import VoteService

from app.schemas import (
    VoteCreate,
    PostVoteOut,
    CommentVoteOut,
)

router = APIRouter(
    prefix="/votes",
    tags=["votes"],
)

service = VoteService()


@router.post(
    "/posts/{post_u_id}",
    response_model=PostVoteOut,
)
def vote_post(
    post_id: UUID,
    vote: VoteCreate,
    db: Session = Depends(get_db),
):
    return service.vote_post(
        db,
        post_id,
        vote,
    )


@router.post(
    "/comments/{comment_u_id}",
    response_model=CommentVoteOut,
)
def vote_comment(
    comment_id: UUID,
    vote: VoteCreate,
    db: Session = Depends(get_db),
):
    return service.vote_comment(
        db,
        comment_id,
        vote,
    )
