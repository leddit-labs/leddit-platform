import httpx


class BaseClient:
    def __init__(self, base_url: str, token: str = None):
        self.base_url = base_url

        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        self.client = httpx.AsyncClient(
            base_url=base_url,
            headers=headers,
            timeout=10,
        )

    async def get(self, path: str):
        r = await self.client.get(path)
        r.raise_for_status()
        return r.json()

    async def post(self, path: str, data: dict):
        r = await self.client.post(path, json=data)
        r.raise_for_status()
        print("POST:", self.base_url + path, data)
        return r.json()

    async def close(self):
        await self.client.aclose()