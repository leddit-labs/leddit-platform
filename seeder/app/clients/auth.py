# app/auth.py
import httpx

KEYCLOAK_URL = "http://keycloak:8080"

async def get_token(username: str, password: str) -> str:
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{KEYCLOAK_URL}/realms/leddit/protocol/openid-connect/token",
            data={
                "grant_type": "password",
                "client_id": "leddit-frontend",
                "username": username,
                "password": password,
            },
        )
        r.raise_for_status()
        return r.json()["access_token"]