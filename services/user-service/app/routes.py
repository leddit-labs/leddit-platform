from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import User
from app.schemas import UserProfile, UserUpdate
from app.security import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserProfile)
async def get_my_profile(user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Get current user's profile. Creates user if first time."""
    result = await db.execute(select(User).where(User.keycloak_id == user["sub"]))
    db_user = result.scalar_one_or_none()
    
    if not db_user:
        db_user = User(
            id=user["sub"],
            keycloak_id=user["sub"],
            username=user["username"],
            display_name=user["username"],
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
    
    return db_user

@router.patch("/me", response_model=UserProfile)
async def update_profile(
    update: UserUpdate,
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update display name or bio."""
    result = await db.execute(select(User).where(User.keycloak_id == user["sub"]))
    db_user = result.scalar_one_or_none()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if update.display_name is not None:
        db_user.display_name = update.display_name
    if update.bio is not None:
        db_user.bio = update.bio
    if update.avatar_url is not None:
        db_user.avatar_url = update.avatar_url
    
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.get("/{user_id}", response_model=UserProfile)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    """Get a user's public profile."""
    result = await db.execute(select(User).where(User.id == user_id))
    db_user = result.scalar_one_or_none()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user