# app/models/user_models.py

from pydantic import BaseModel, EmailStr, Field

class UserSignup(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8)
    email: EmailStr
