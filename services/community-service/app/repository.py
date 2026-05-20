from uuid import uuid4
from sqlalchemy.orm import Session
from app.models import Community, CommunityModerator, CommunityRule, ModeratorRole
from app.schemas import CommunityCreate, CommunityUpdate, RuleIn, RuleUpdate

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


# ----------------
# Rules
# ----------------
def get_rules(db: Session, community_id: str) -> list[CommunityRule]:
    return (
        db.query(CommunityRule)
        .filter(CommunityRule.community_id == community_id)
        .order_by(CommunityRule.order)
        .all()
    )


def count_rules(db: Session, community_id: str) -> int:
    return (
        db.query(CommunityRule)
        .filter(CommunityRule.community_id == community_id)
        .count()
    )

def add_rule(db: Session, community_id: str, rule: RuleIn) -> CommunityRule:
    r = CommunityRule(
        id=uuid4().hex[:12],
        community_id=community_id,
        order=count_rules(db, community_id) + 1,
        title=rule.title,
        text=rule.text,
    )
    db.add(r)
    db.commit()
    db.refresh(r)
    return r

def get_rule(db: Session, community_id: str, rule_id: str) -> CommunityRule | None:
    return (
        db.query(CommunityRule)
        .filter(CommunityRule.community_id == community_id, CommunityRule.id == rule_id)
        .first()
    )

def update_rule(db: Session, rule: CommunityRule, data: RuleUpdate) -> CommunityRule:
    if data.title is not None:
        rule.title = data.title
    if data.text is not None:
        rule.text = data.text
    db.commit()
    db.refresh(rule)
    return rule


def delete_rule(db: Session, rule: CommunityRule) -> None:
    community_id = rule.community_id
    removed_order = rule.order

    db.delete(rule)

    db.query(CommunityRule).filter(
        CommunityRule.community_id == community_id,
        CommunityRule.order > removed_order,
    ).update({CommunityRule.order: CommunityRule.order - 1})
    db.commit()

