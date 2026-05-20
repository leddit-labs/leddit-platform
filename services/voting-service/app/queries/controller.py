from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.db_read import get_read_db

from app.queries.models import PostVoteSummary, CommentVoteSummary, UserCommentVote, UserPostVote
from app.queries.schemas import PostVoteSummaryOut, CommentVoteSummaryOut, UserVoteOut

router = APIRouter(
    prefix="/votes",
    tags=["votes"],
)


@router.get(
    "/posts/{post_id}",
    response_model=PostVoteSummaryOut,
)
def get_post_votes(
    post_id: UUID,
    db: Session = Depends(get_read_db),
):
    vote_summary = db.get(PostVoteSummary, post_id)

    if not vote_summary:
        raise HTTPException(
            status_code=404,
            detail="Post vote summary not found",
        )

    return vote_summary

@router.get(
    "/comments/{comment_id}",
    response_model=CommentVoteSummaryOut,
)
def get_comment_votes(
    comment_id: UUID,
    db: Session = Depends(get_read_db),
):
    vote_summary = db.get(CommentVoteSummary, comment_id)

    if not vote_summary:
        raise HTTPException(
            status_code=404,
            detail="Comment vote summary not found",
        )

    return vote_summary

@router.get(
    "/posts/{post_id}/me",
    response_model=UserVoteOut,
)
def get_user_post_vote(
    post_id: UUID,
    user_id: UUID,
    db: Session = Depends(get_read_db),
):
    vote = (
        db.query(UserPostVote)
        .filter(
            UserPostVote.post_id == post_id,
            UserPostVote.user_id == user_id,
        )
        .first()
    )

    if not vote:
        return {"value": 0} # 0 means that user have not voted on this post

    return {"value": vote.value}


@router.get(
    "/comments/{comment_id}/me",
    response_model=UserVoteOut,
)
def get_user_comment_vote(
    comment_id: UUID,
    user_id: UUID,
    db: Session = Depends(get_read_db),
):
    vote = (
        db.query(UserCommentVote)
        .filter(
            UserCommentVote.comment_id == comment_id,
            UserCommentVote.user_id == user_id,
        )
        .first()
    )

    if not vote:
        return {"value": 0} # 0 means that user have not voted on this comment

    return {"value": vote.value}