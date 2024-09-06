from fastapi import APIRouter
from app.core.security import verify_token

router = APIRouter()


@router.post("/")
async def validate_token(token: str):
    try:
        user_info = await verify_token(token)
        return {"success": True, "user_info": user_info}
    except Exception as e:
        return {"success": False, "message": str(e)}
