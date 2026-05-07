from uuid import uuid4
from sqlalchemy.orm import Session
from app.models import Community
from app.schemas import CommunityCreate, CommunityUpdate


def create(db: Session, data: CommunityCreate) -> Community:
    community = Community(
        id=uuid4().hex[:12],
        name=data.name,
        description=data.description,
    )
    db.add(community)
    db.commit()
    db.refresh(community)
    return community


def get_all(db: Session) -> list[Community]:
    return db.query(Community).all()


def get_by_id(db: Session, community_id: str) -> Community | None:
    return db.query(Community).filter(Community.id == community_id).first()


def get_by_name(db: Session, name: str) -> Community | None:
    return db.query(Community).filter(Community.name == name).first()


def update(db: Session, community: Community, data: CommunityUpdate) -> Community:
    if data.description is not None:
        community.description = data.description
    db.commit()
    db.refresh(community)
    return community


def delete(db: Session, community: Community) -> None:
    db.delete(community)
    db.commit()
