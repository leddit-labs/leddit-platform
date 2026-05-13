from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt, JWTError
import httpx
from app.config import settings

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{settings.keycloak_url}/realms/{settings.keycloak_realm}/protocol/openid-connect/auth",
    tokenUrl=f"{settings.keycloak_url}/realms/{settings.keycloak_realm}/protocol/openid-connect/token",
)

async def get_public_key() -> dict:
    """Fetch Keycloak public key for JWT validation."""
    certs_url = f"{settings.keycloak_url}/realms/{settings.keycloak_realm}/protocol/openid-connect/certs"
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(certs_url)
        response.raise_for_status()
        jwks = response.json()
        
        if "keys" not in jwks or len(jwks["keys"]) == 0:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No keys found in JWKS"
            )
        
        return jwks["keys"][0]

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Validate JWT and return user info."""
    try:
        public_key = await get_public_key()
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            options={"verify_aud": False}
        )
        return {
            "sub": payload.get("sub"),
            "username": payload.get("preferred_username"),
            "email": payload.get("email"),
        }
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Auth error: {str(e)}"
        )