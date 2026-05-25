from .base import BaseClient


class UserClient(BaseClient):
    async def get_profile(self):
        return await self.get("/users/me")