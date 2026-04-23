from fastapi import Request
from app.security import decode_token
from sqlalchemy import select
from app.db import AsyncSessionLocal
from app.models import User

async def get_current_user(info):
    request: Request = info.context["request"]
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    payload = decode_token(token)
    user_id = payload.get("sub")
    if not user_id:
        return None
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.id == int(user_id)))
        return result.scalar_one_or_none()