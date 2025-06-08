# app/routers/auth.py

# FastAPI Core
from fastapi import APIRouter, HTTPException, Depends

# Internal Models
from app.models.user_models import (
    UserSignup,
    UserLogin,
    ConfirmSignup,
    ResendCodeRequest,
)

# Services & Utils
from app.services.cognito_service import cognito_service
from app.utils.jwt_utils import get_current_user


router = APIRouter()


@router.post("/signup")
def signup(user: UserSignup):
    try:
        result = cognito_service.sign_up_user(
            username=user.username, password=user.password, email=user.email
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(user: UserLogin):
    try:
        result = cognito_service.login_user(
            username=user.username, password=user.password
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/confirm")
def confirm(user: ConfirmSignup):
    try:
        result = cognito_service.confirm_user(username=user.username, code=user.code)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/profile")
def get_profile(user: dict = Depends(get_current_user)):
    return {
        "message": "Welcome to your profile!",
        "user": {
            "username": user.get("cognito:username"),
            "email": user.get("email"),
            "sub": user.get("sub"),
        },
    }


@router.post("/resend-code")
def resend_code(data: ResendCodeRequest):
    try:
        result = cognito_service.resend_confirmation_code(username=data.username)
        return {"message": "Confirmation code resent successfully", "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
