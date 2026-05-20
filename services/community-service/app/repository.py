from uuid import uuid4
from sqlalchemy.orm import Session
from app.models import Community, CommunityModerator, ModeratorRole
from app.schemas import CommunityCreate, CommunityUpdate

# ----------------
# Community CRUD
# ----------------
def create(db: Session, data: CommunityCreate, created_by: str) -> Community:
    community = Community(
        id=uuid4().hex[:12],
        name=data.name,
        description=data.description,
        created_by=created_by,
    )
    db.add(community)
 
    owner = CommunityModerator(
        community_id=community.id,
        user_id=created_by,
        role=ModeratorRole.owner,
    )
    db.add(owner)
 
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

# ----------------
# Moderator stuff
# ----------------
def get_moderator(db: Session, community_id: str, user_id: str) -> CommunityModerator | None:
    return (
        db.query(CommunityModerator)
        .filter(
            CommunityModerator.community_id == community_id,
            CommunityModerator.user_id == user_id,
        )
        .first()
    )

def get_moderators(db: Session, community_id: str) -> list[CommunityModerator]:
    return (
        db.query(CommunityModerator)
        .filter(CommunityModerator.community_id == community_id)
        .all()
    )


def add_moderator(db: Session, community_id: str, user_id: str) -> CommunityModerator:
    mod = CommunityModerator(
        community_id=community_id,
        user_id=user_id,
        role=ModeratorRole.moderator,
    )
    db.add(mod)
    db.commit()
    db.refresh(mod)
    return mod


def remove_moderator(db: Session, mod: CommunityModerator) -> None:
    db.delete(mod)
    db.commit()


def is_owner(db: Session, community_id: str, user_id: str) -> bool:
    mod = get_moderator(db, community_id, user_id)
    return mod is not None and mod.role == ModeratorRole.owner


def is_moderator_or_owner(db: Session, community_id: str, user_id: str) -> bool:
    return get_moderator(db, community_id, user_id) is not None

