# app/config/settings.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    cognito_user_pool_id: str
    cognito_client_id: str
    cognito_client_secret: str
    aws_region: str

    class Config:
        env_file = ".env"

settings = Settings()
