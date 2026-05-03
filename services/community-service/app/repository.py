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
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        include_private: bool = False,
    ) -> tuple[list[Community], int]:
        query = select(Community).where(Community.is_archived.is_(False))
        if not include_private:
            query = query.where(Community.is_private.is_(False))

        total_result = await self._session.execute(
            select(func.count()).select_from(query.subquery())
        )
        total = total_result.scalar_one()

        query = query.order_by(Community.created_at.desc())
        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self._session.execute(query)
        return result.scalars().all(), total

    # Memberships

    async def add_member(
        self, community_id: uuid.UUID, user_id: uuid.UUID
    ) -> CommunityMember:
        member = CommunityMember(community_id=community_id, user_id=user_id)
        self._session.add(member)
        await self._session.flush()
        await self._session.refresh(member)
        return member

    async def remove_member(self, community_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        result = await self._session.execute(
            delete(CommunityMember).where(
                CommunityMember.community_id == community_id,
                CommunityMember.user_id == user_id,
            )
        )
        await self._session.flush()
        return result.rowcount > 0

    async def get_membership(
        self, community_id: uuid.UUID, user_id: uuid.UUID
    ) -> CommunityMember | None:
        result = await self._session.execute(
            select(CommunityMember).where(
                CommunityMember.community_id == community_id,
                CommunityMember.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def list_members(self, community_id: uuid.UUID) -> list[CommunityMember]:
        result = await self._session.execute(
            select(CommunityMember)
            .where(CommunityMember.community_id == community_id)
            .order_by(CommunityMember.joined_at)
        )
        return result.scalars().all()
