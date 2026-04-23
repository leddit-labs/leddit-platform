from sqlalchemy import Column, Integer, String, DateTime, Enum, Text, Boolean
from sqlalchemy.sql import func
from app.db import Base
import enum

class UserRole(str, enum.Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    bio = Column(Text, nullable=True)
    karma = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"
    id = Column(Integer, primary_key=True)
    jti = Column(String(36), unique=True, index=True)
    expires_at = Column(DateTime(timezone=True))