from .base import BaseClient

class PostClient(BaseClient):
    async def create(self, data):
        return await self.post("/posts", data)