from fastapi import HTTPException
from pydantic import BaseModel
from jose import jwt, JWTError
from app.redis_client import redis_client
from app.config import settings
import json

class VerifyResponse(BaseModel):
    valid: bool
    user_id: int | None = None
    role: str | None = None

async def verify_token(token: str, use_cache: bool = True) -> VerifyResponse:
    if use_cache:
        cached = await redis_client.get(f"verify:{token}")
        if cached:
            data = json.loads(cached)
            return VerifyResponse(**data)
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        jti = payload.get("jti")
        if jti and await redis_client.exists(f"blacklist:{jti}"):
            raise JWTError("Token blacklisted")
        
        user_id = payload.get("sub")
        role = payload.get("role")
        if not user_id:
            raise JWTError("Missing subject")
        
        response = VerifyResponse(valid=True, user_id=int(user_id), role=role)
    except JWTError:
        response = VerifyResponse(valid=False, user_id=None, role=None)
    
    if response.valid and use_cache:
        await redis_client.setex(f"verify:{token}", settings.CACHE_TTL_SECONDS, response.json())
    return response