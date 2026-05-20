import enum

from sqlalchemy import Column, Enum, ForeignKey, String, UniqueConstraint
from app.database import Base


class ModeratorRole(str, enum.Enum):
    owner = "owner"
    moderator = "moderator"

class Community(Base):
    __tablename__ = "communities"

    id = Column(String, primary_key=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(500), default="")
    created_by = Column(String, nullable=False, index=True)

class CommunityModerator(Base):
    __tablename__ = "community_moderators"

    community_id = Column(String, ForeignKey("communities.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(String, primary_key=True)
    role = Column(Enum(ModeratorRole), nullable=False)
 
    __table_args__ = (
        UniqueConstraint("community_id", "user_id", name="uq_community_user"),
    )
