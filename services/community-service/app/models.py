from sqlalchemy import Column, String
from app.database import Base


class Community(Base):
    __tablename__ = "communities"

    id = Column(String, primary_key=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(500), default="")
