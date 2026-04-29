import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.db import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    u_id = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4, index=True)

    community_id = Column(UUID(as_uuid=True))
    author_id = Column(UUID(as_uuid=True))

    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    deleted_at = Column(DateTime, nullable=True)
