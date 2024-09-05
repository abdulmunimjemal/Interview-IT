from fastapi import APIRouter, Depends, HTTPException
from app.services.firebase_service import FirebaseService
from app.models.user import UserCreate, UserLogin
from app.core.security import create_access_token

router = APIRouter()
firebase_service = FirebaseService()

@router.post("/register")
async def register_user(user: UserCreate):
    try:
        firebase_service.register_user(user.email, user.password)
        return {"success": True, "message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login_user(user: UserLogin):
    try:
        user_data = firebase_service.login_user(user.email, user.password)
        access_token = create_access_token(data={"user_id": user_data["localId"]})
        return {"success": True, "access_token": access_token, "refresh_token": user_data["refreshToken"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/refresh-token")
async def refresh_token(refresh_token: str):
    try:
        new_token = firebase_service.refresh_token(refresh_token)
        return {"success": True, "access_token": new_token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))