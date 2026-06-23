import asyncio
import httpx

from app.config import endpoints


SERVICES = {
	"users": f"{endpoints.USERS}/health",
	"communities": f"{endpoints.COMMUNITIES}/health",
	"posts": f"{endpoints.POSTS}/health",
	"comments": f"{endpoints.COMMENTS}/health",
	"votes": f"{endpoints.VOTES}/health",
	"keycloak": f"{endpoints.KEYCLOAK}/realms/master",
}


async def wait_for_service(client, name, url):
    for _ in range(30):
        try:
            r = await client.get(url)
            if r.status_code == 200:
                print(f"[READY] {name}")
                return
        except Exception:
            pass

        await asyncio.sleep(2)

    raise RuntimeError(f"{name} not healthy on: {url}")


async def wait_for_services():
	async with httpx.AsyncClient(timeout=5) as client:
		await asyncio.gather(*[
			wait_for_service(client, name, url)
			for name, url in SERVICES.items()
		])