import uuid

from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    UniqueConstraint,
)

from sqlalchemy.dialects.postgresql import UUID

from app.db import Base


class PostVote(Base):
    __tablename__ = "post_votes"

    # is this even needed if user_u_id is unique?
    __table_args__ = (
        UniqueConstraint(
            "post_id",
            "user_id",
            name="uq_post_vote",
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)

    u_id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        unique=True,
        index=True,
    )

    post_id = Column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
    )

    user_id = Column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
    )

    value = Column(Integer, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
    )



class CommentVote(Base):
    __tablename__ = "comment_votes"

    # is this even needed if user_u_id is unique?
    __table_args__ = (
        UniqueConstraint(
            "comment_id",
            "user_id",
            name="uq_comment_vote",
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        unique=True,
        index=True,
    )

    comment_id = Column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
    )

    user_id = Column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
    )

    value = Column(Integer, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
    )

