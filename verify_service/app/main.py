from fastapi import FastAPI, Header, HTTPException
from app.verify import verify_token
from app.config import settings

app = FastAPI(title="Token Verify Service")

@app.post("/verify")
async def verify(authorization: str = Header(...)):
    """
    Internal endpoint for other services.
    Expects: Authorization: Bearer <token>
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid authorization header")
    token = authorization.split(" ")[1]
    result = await verify_token(token)
    if not result.valid:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return result

@app.get("/health")
async def health():
    return {"status": "ok"}