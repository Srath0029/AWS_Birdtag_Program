from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    cognito_user_pool_id: str
    cognito_client_id: str
    cognito_client_secret: str
    aws_region: str
    aws_access_key_id: str
    aws_secret_access_key: str
    s3_bucket_name: str
  

    class Config:
        env_file = ".env"

settings = Settings()
