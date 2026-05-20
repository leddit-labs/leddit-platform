from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.db_read import get_read_db

from app.queries.models import PostVoteSummary, CommentVoteSummary, UserPostVote
from app.queries.schemas import PostVoteSummaryOut, CommentVoteSummaryOut

router = APIRouter(
    prefix="/votes",
    tags=["votes"],
)


@router.get(
    "/test",
)
def test():
    get_read_db()
    return "test"

@router.get("/{post_id}", response_model=PostVoteSummaryOut)
def get_post_votes(post_id: UUID, db: Session = Depends(get_read_db)):
    return db.get(PostVoteSummary, post_id)

@router.get("/{comment_id}", response_model=CommentVoteSummaryOut)
def get_comment_votes(comment_id: UUID, db: Session = Depends(get_read_db)):
    return db.get(CommentVoteSummary, comment_id)

@router.get("/posts/{post_id}/me")
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
        return {"value": 0}

    return {"value": vote.value}