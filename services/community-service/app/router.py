import base64 
import json
import logging

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    CommunityCreate,
    CommunityUpdate,
    CommunityOut,
    ModeratorAdd,
    ModeratorOut,
    RuleIn,
    RuleUpdate,
    RuleOut,
)
from app import repository
from app.messaging import publish_event

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/communities", tags=["communities"])

# ----------------------------------------------------
# HELPER FUNCTIONS
# ----------------------------------------------------
def get_current_user(
    authorization: str | None = Header(None)
) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing or invalid authorization")
    token = authorization.split(" ", 1)[1]
    payload = json.loads(base64.urlsafe_b64decode(token.split(".")[1] + "=="))
    return payload["sub"]

# ----------------------------------------------------
# Write protected routes (POST, PUT, PATCH, DELETE)
# ----------------------------------------------------
@router.post("", response_model=CommunityOut, status_code=201)
def create_community(
    body: CommunityCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    if repository.get_by_name(db, body.name):
        raise HTTPException(409, "Community name already exists")

    community = repository.create(db, body, created_by=user_id)
    logger.info("Community created", extra={"community_id": community.id, "community_name": body.name, "user_id": user_id})
    # publish full community payload for consumers
    publish_event(
        "community_created",
        {
            "u_id": community.id,
            "name": community.name,
            "description": community.description,
            "created_by": community.created_by,
        }
    )
    return community


@router.put("/{community_id}", response_model=CommunityOut)
def update_community(
    community_id: str,
    body: CommunityUpdate, 
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    community = repository.get_by_id(db, community_id)
    if not community:
        raise HTTPException(404, "Community not found")
    if not repository.is_moderator_or_owner(db, community_id, user_id):
        logger.warning("Unauthorized change attempt", extra={"community_id": community_id, "user_id": user_id})
        raise HTTPException(403, "Only moderators can update a community")
    community_updated = repository.update(db, community, body)
    publish_event(
        "community_updated",
        {
            "u_id": community_updated.id,
            "name": community_updated.name,
            "description": community_updated.description,
            "created_by": community_updated.created_by,
        }
    )
    return community_updated


@router.delete("/{community_id}", status_code=204)
def delete_community(
        community_id: str,
        db: Session = Depends(get_db),
        user_id: str = Depends(get_current_user),
):
    community_deleted = repository.get_by_id(db, community_id)
    if not community_deleted:
        raise HTTPException(404, "Community not found")
    if not repository.is_owner(db, community_id, user_id):
        logger.warning("Unauthorized delete attempt", extra={"community_id": community_id, "user_id": user_id})
        raise HTTPException(403, "Only the owner can delete a community")
    repository.delete(db, community_deleted)
    publish_event(
        "community_deleted", 
            {
                "u_id": community_deleted.id
            }
        )


# ----------------------------------------------------
# Public read routes (GET)
# ----------------------------------------------------
@router.get("", response_model=list[CommunityOut])
def list_communities(db: Session = Depends(get_db)):
    return repository.get_all(db)


@router.get("/{community_id}", response_model=CommunityOut)
def get_community(community_id: str, db: Session = Depends(get_db)):
    community = repository.get_by_id(db, community_id)
    if not community:
        raise HTTPException(404, "Community not found")
    return community


# ----------------------------------------------------
# Moderator Management
# ----------------------------------------------------
@router.get("/{community_id}/moderators", response_model=list[ModeratorOut])
def list_moderators(community_id: str, db: Session = Depends(get_db)):
    community = repository.get_by_id(db, community_id)
    if not community:
        raise HTTPException(404, "Community not found")
    return repository.get_moderators(db, community_id)


@router.post("/{community_id}/moderators", response_model=ModeratorOut, status_code=201)
def add_moderator(
    community_id: str,
    body: ModeratorAdd,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    community = repository.get_by_id(db, community_id)
    if not community:
        raise HTTPException(404, "Community not found")
    if not repository.is_owner(db, community_id, user_id):
        raise HTTPException(403, "Only the owner can add moderators")
    if repository.get_moderator(db, community_id, body.user_id):
        raise HTTPException(409, "User is already a moderator or owner")
    return repository.add_moderator(db, community_id, body.user_id)


@router.delete("/{community_id}/moderators/{target_user_id}", status_code=204)
def remove_moderator(
    community_id: str,
    target_user_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    community = repository.get_by_id(db, community_id)
    if not community:
        raise HTTPException(404, "Community not found")
    if not repository.is_owner(db, community_id, user_id):
        raise HTTPException(403, "Only the owner can remove moderators")
    mod = repository.get_moderator(db, community_id, target_user_id)
    if not mod:
        raise HTTPException(404, "Moderator not found")
    if mod.role.value == "owner":
        raise HTTPException(400, "Cannot remove the owner")
    repository.remove_moderator(db, mod)


# ----------------------------------------------------
# Rules
# ----------------------------------------------------
@router.get("/{community_id}/rules", response_model=list[RuleOut])
def list_rules(community_id: str, db: Session = Depends(get_db)):
    community = repository.get_by_id(db, community_id)
    if not community:
        raise HTTPException(404, "Community not found")
    return repository.get_rules(db, community_id)


@router.post("/{community_id}/rules", response_model=RuleOut, status_code=201)
def add_rule(
    community_id: str,
    body: RuleIn,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    community = repository.get_by_id(db, community_id)
    if not community:
        raise HTTPException(404, "Community not found")
    if not repository.is_moderator_or_owner(db, community_id, user_id):
        raise HTTPException(403, "Only moderators can manage rules")
    if repository.count_rules(db, community_id) >= 20:
        raise HTTPException(400, "A community can have at most 20 rules")
    return repository.add_rule(db, community_id, body)


@router.patch("/{community_id}/rules/{rule_id}", response_model=RuleOut)
def update_rule(
    community_id: str,
    rule_id: str,
    body: RuleUpdate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    community = repository.get_by_id(db, community_id)
    if not community:
        raise HTTPException(404, "Community not found")
    if not repository.is_moderator_or_owner(db, community_id, user_id):
        raise HTTPException(403, "Only moderators can manage rules")
    rule = repository.get_rule(db, community_id, rule_id)
    if not rule:
        raise HTTPException(404, "Rule not found")
    return repository.update_rule(db, rule, body)


@router.delete("/{community_id}/rules/{rule_id}", status_code=204)
def delete_rule(
    community_id: str,
    rule_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    community = repository.get_by_id(db, community_id)
    if not community:
        raise HTTPException(404, "Community not found")
    if not repository.is_moderator_or_owner(db, community_id, user_id):
        raise HTTPException(403, "Only moderators can manage rules")
    rule = repository.get_rule(db, community_id, rule_id)
    if not rule:
        raise HTTPException(404, "Rule not found")
    repository.delete_rule(db, rule)

