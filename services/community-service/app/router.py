from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import CommunityCreate, CommunityUpdate, CommunityOut
from app import repository

router = APIRouter(prefix="/communities", tags=["communities"])


@router.post("", response_model=CommunityOut, status_code=201)
def create_community(body: CommunityCreate, db: Session = Depends(get_db)):
    if repository.get_by_name(db, body.name):
        raise HTTPException(409, "Community name already exists")
    return repository.create(db, body)


@router.get("", response_model=list[CommunityOut])
def list_communities(db: Session = Depends(get_db)):
    return repository.get_all(db)


@router.get("/{community_id}", response_model=CommunityOut)
def get_community(community_id: str, db: Session = Depends(get_db)):
    community = repository.get_by_id(db, community_id)
    if not community:
        raise HTTPException(404, "Community not found")
    return community


@router.put("/{community_id}", response_model=CommunityOut)
def update_community(
    community_id: str, body: CommunityUpdate, db: Session = Depends(get_db)
):
    community = repository.get_by_id(db, community_id)
    if not community:
        raise HTTPException(404, "Community not found")
    return repository.update(db, community, body)


@router.delete("/{community_id}", status_code=204)
def delete_community(community_id: str, db: Session = Depends(get_db)):
    community = repository.get_by_id(db, community_id)
    if not community:
        raise HTTPException(404, "Community not found")
    repository.delete(db, community)
