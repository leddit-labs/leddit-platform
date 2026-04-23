import strawberry
from sqlalchemy import select
from app.db import AsyncSessionLocal
from app.models import User
from app.security import hash_password, verify_password, create_access_token, blacklist_token, decode_token
from app.graphql.types import RegisterInput, LoginInput, AuthPayload, Message
from datetime import datetime, timezone

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def register(self, input: RegisterInput) -> AuthPayload:
        async with AsyncSessionLocal() as session:
            existing = await session.execute(
                select(User).where((User.email == input.email) | (User.username == input.username))
            )
            if existing.scalar_one_or_none():
                raise Exception("User already exists")
            print(f"Password length (bytes): {len(input.password.encode('utf-8'))}")
            print(input.password)
            hashed = hash_password(input.password)
            user = User(email=input.email, username=input.username, hashed_password=hashed)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            
            token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
            return AuthPayload(access_token=token, token_type="bearer")

    @strawberry.mutation
    async def login(self, input: LoginInput) -> AuthPayload:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User).where(User.username == input.username))
            user = result.scalar_one_or_none()
            if not user or not verify_password(input.password, user.hashed_password):
                raise Exception("Invalid credentials")
            
            token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
            return AuthPayload(access_token=token, token_type="bearer")

    @strawberry.mutation
    async def logout(self, token: str) -> Message:
        payload = decode_token(token)
        if not payload:
            raise Exception("Invalid token")
        jti = payload.get("jti")
        exp = payload.get("exp")
        if jti and exp:
            expires_at = datetime.fromtimestamp(exp, tz=timezone.utc)
            await blacklist_token(jti, expires_at)
        return Message(message="Logged out successfully")