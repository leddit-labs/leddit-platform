from .base import BaseClient


class UserClient(BaseClient):
    async def create(self, data):
        return await self.post("/users", data)