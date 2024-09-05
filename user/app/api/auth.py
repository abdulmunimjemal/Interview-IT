from fastapi import APIRouter, Depends, HTTPException
from app.services.firebase_service import FirebaseService
from app.models.user import UserCreate, UserLogin
from app.core.security import create_access_token, verify_token

router = APIRouter()
firebase_service = FirebaseService()

@router.post("/register")
async def register_user(user: UserCreate):
    try:
        firebase_service.register_user(user.email, user.password)
        return {"success": True, "message": "User registered successfully. A verification email has been sent."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login_user(user: UserLogin):
    try:
        user_data = firebase_service.login_user(user.email, user.password)
        access_token = create_access_token(data={"user_id": user_data["localId"]})
        return {"success": True, "access_token": access_token, "refresh_token": user_data["refreshToken"]}
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/refresh-token")
async def refresh_token(refresh_token: str):
    try:
        new_token = firebase_service.refresh_token(refresh_token)
        return {"success": True, "access_token": new_token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/delete-user")
async def delete_user(user=Depends(verify_token)):
    try:
        uid = user.get("user_id")
        firebase_service.delete_user(uid)
        return {"success": True, "message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/change-password")
async def change_password(new_password: str, user=Depends(verify_token)):
    try:
        id_token = user.get("id_token")
        firebase_service.change_password(id_token, new_password)
        return {"success": True, "message": "Password changed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/check-email-verification")
async def check_email_verification(user=Depends(verify_token)):
    try:
        user_info = firebase_service.auth.get_account_info(user.get("id_token"))
        email_verified = user_info['users'][0]['emailVerified']
        return {"email_verified": email_verified}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))