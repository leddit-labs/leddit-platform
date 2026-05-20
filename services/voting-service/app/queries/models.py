from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.db_read import Base


class PostVoteSummary(Base):
    __tablename__ = "post_vote_summaries"

    post_id = Column(UUID(as_uuid=True), primary_key=True)

    upvotes = Column(Integer, default=0, nullable=False)
    downvotes = Column(Integer, default=0, nullable=False)

    score = Column(Integer, default=0, nullable=False)

    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class CommentVoteSummary(Base):
    __tablename__ = "comment_vote_summaries"

    comment_id = Column(UUID(as_uuid=True), primary_key=True)

    upvotes = Column(Integer, default=0, nullable=False)
    downvotes = Column(Integer, default=0, nullable=False)

    score = Column(Integer, default=0, nullable=False)

    updated_at = Column(
        DateTime(timezone=True), onupdate=func.now()
    )


class UserPostVote(Base):
    __tablename__ = "user_post_votes"

    user_id = Column(UUID(as_uuid=True), primary_key=True)
    post_id = Column(UUID(as_uuid=True), primary_key=True)

    value = Column(Integer, nullable=False) # -1, 1, 0


class UserCommentVote(Base):
    __tablename__ = "user_comment_votes"

    user_id = Column(UUID(as_uuid=True), primary_key=True)
    comment_id = Column(UUID(as_uuid=True), primary_key=True)

    value = Column(Integer, nullable=False) # -1, 1, 0
