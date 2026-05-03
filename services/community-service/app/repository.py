import uuid

from sqlalchemy import func, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Community, CommunityMember, CommunityModerator, CommunityRule


class CommunityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # Communities

    async def create(self, **kwargs) -> Community:
        community = Community(**kwargs)
        self._session.add(community)
        await self._session.flush()
        await self._session.refresh(community)
        return community

    async def get_by_id(self, community_id: uuid.UUID) -> Community | None:
        result = await self._session.execute(
            select(Community).where(Community.id == community_id)
        )
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Community | None:
        result = await self._session.execute(
            select(Community).where(Community.slug == slug)
        )
        return result.scalar_one_or_none()

    async def slug_exists(self, slug: str) -> bool:
        result = await self._session.execute(
            select(Community.id).where(Community.slug == slug)
        )
        return result.scalar_one_or_none() is not None

    async def list_communities(
        self, *, page: int = 1, page_size: int = 20
    ) -> tuple[list[Community], int]:
        query = select(Community).where(Community.is_deleted == False)
