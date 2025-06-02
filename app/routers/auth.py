# app/routers/auth.py

from fastapi import APIRouter, HTTPException
from app.models.user_models import UserSignup
from app.models.user_models import UserLogin
from app.models.user_models import ConfirmSignup
from app.services.cognito_service import cognito_service

router = APIRouter()

@router.post("/signup")
def signup(user: UserSignup):
    try:
        result = cognito_service.sign_up_user(
            username=user.username,
            password=user.password,
            email=user.email
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(user: UserLogin):
    try:
        result = cognito_service.login_user(
            username=user.username,
            password=user.password
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/confirm")
def confirm(user: ConfirmSignup):
    try:
        result = cognito_service.confirm_user(
            username=user.username,
            code=user.code
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))