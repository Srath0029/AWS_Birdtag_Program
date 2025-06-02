# app/routers/auth.py

from fastapi import APIRouter, HTTPException
from app.models.user_models import UserSignup
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
