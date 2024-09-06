from fastapi import HTTPException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from app.core.config import settings

security = HTTPBearer()


def create_access_token(data: dict):
    return jwt.encode(data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


async def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str | None = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
