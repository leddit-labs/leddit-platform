from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt, JWTError
from jose import jwk
import httpx
from app.config import settings
import logging
import base64
import json

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{settings.keycloak_url}/realms/{settings.keycloak_realm}/protocol/openid-connect/auth",
    tokenUrl=f"{settings.keycloak_url}/realms/{settings.keycloak_realm}/protocol/openid-connect/token",
)

_cached_keys = None

async def get_current_user_from_gateway(
    authorization: str = Header(None),
):
    """Token already validated by APISIX. Extract user from JWT payload."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header"
        )
    
    token = authorization.split(" ")[1]

    try:
        payload = token.split(".")[1]
        payload += "=" * (4 - len(payload) % 4)
        decoded = base64.urlsafe_b64decode(payload)
        user_data = json.loads(decoded)
        
        return {
            "sub": user_data["sub"],
            "username": user_data.get("preferred_username"),
            "email": user_data.get("email"),
        }
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing required 'sub' claim"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format"
        )

async def get_public_keys() -> list:
    """Fetch ALL Keycloak public keys with caching."""
    global _cached_keys
    if _cached_keys is not None:
        return _cached_keys
    
    certs_url = f"{settings.keycloak_url}/realms/{settings.keycloak_realm}/protocol/openid-connect/certs"
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(certs_url)
        response.raise_for_status()
        jwks = response.json()
        _cached_keys = jwks.get("keys", [])
        return _cached_keys

def get_key_for_token(token: str, keys: list) -> dict:
    """Find the correct key matching the token's kid."""
    header = jwt.get_unverified_header(token)
    kid = header.get("kid")
    
    for key in keys:
        if key.get("kid") == kid:
            return key
    
    if keys:
        return keys[0]
    
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="No keys available"
    )

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Validate JWT and return user info."""
    try:
        keys = await get_public_keys()
        public_key = get_key_for_token(token, keys)
        
        if "x5c" in public_key:
            cert = f"-----BEGIN CERTIFICATE-----\n{public_key['x5c'][0]}\n-----END CERTIFICATE-----"
            payload = jwt.decode(
                token,
                cert,
                algorithms=["RS256"],
                options={"verify_aud": False}
            )
        else:
            key = jwk.construct(public_key, "RS256").to_pem()
            payload = jwt.decode(
                token,
                key,
                algorithms=["RS256"],
                options={"verify_aud": False}
            )
        
        return {
            "sub": payload["sub"],
            "username": payload.get("preferred_username"),
            "email": payload.get("email"),
        }
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing required 'sub' claim"
        )
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