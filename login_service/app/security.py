from datetime import datetime, timedelta, timezone
from jose import jwt
import bcrypt
from app.config import settings
import redis.asyncio as redis

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')[:72]
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_bytes = plain_password.encode('utf-8')[:72]
    return bcrypt.checkpw(plain_bytes, hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    import uuid
    to_encode["jti"] = str(uuid.uuid4())
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except jwt.JWTError:
        return {}

async def blacklist_token(jti: str, expires_at: datetime):
    ttl = int((expires_at - datetime.now(timezone.utc)).total_seconds())
    if ttl > 0:
        await redis_client.setex(f"blacklist:{jti}", ttl, "1")