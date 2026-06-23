from .base import BaseClient

class VoteClient(BaseClient):
    async def create(self, data):
        return await self.post("/votes", data)