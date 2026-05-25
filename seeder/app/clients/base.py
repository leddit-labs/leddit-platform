import httpx

class BaseClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=10)

    async def get(self, path: str):
        r = await self.client.get(self.base_url + path)
        r.raise_for_status()
        return r.json()

    async def post(self, path: str, data: dict):
        r = await self.client.post(self.base_url + path, json=data)
        r.raise_for_status()
        return r.json()