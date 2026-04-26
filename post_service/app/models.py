import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.db import Base


class Post(Base):
	__tablename__ = "posts"

	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	u_id = Column(UUID(as_uuid=True))
	community_id = Column(UUID(as_uuid=True))
	author_id = Column(UUID(as_uuid=True))

	title = Column(String, nullable=False)
	content = Column(Text, nullable=True)
	#image = Column(String, nullable=True)

	created_at = Column(DateTime, default=datetime.utcnow)
	deleted_at = Column(DateTime, nullable=True)

	score = Column(String, default="0")