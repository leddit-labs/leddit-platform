from .base import BaseClient

class CommunityClient(BaseClient):
    async def create(self, data):
        return await self.post("/communities", data)