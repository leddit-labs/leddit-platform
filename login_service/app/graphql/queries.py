import strawberry
from strawberry.types import Info
from app.graphql.types import UserProfile
from app.graphql.types import UserRole
from app.graphql.context import get_current_user
from app.models import User

@strawberry.type
class Query:
    @strawberry.field
    async def me(self, info: Info) -> UserProfile:
        user = await get_current_user(info)
        if not user:
            raise Exception("Not authenticated")
        return UserProfile(
            id=user.id,
            username=user.username,
            email=user.email,
            bio=user.bio,
            karma=user.karma,
            role=UserRole(user.role.value),
            created_at=user.created_at,
        )