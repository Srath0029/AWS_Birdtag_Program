from jose import jwt
import requests

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config.settings import settings

security = HTTPBearer()

# Download and cache public keys from Cognito
COGNITO_KEYS_URL = f"https://cognito-idp.{settings.aws_region}.amazonaws.com/{settings.cognito_user_pool_id}/.well-known/jwks.json"
jwks = requests.get(COGNITO_KEYS_URL).json()

def decode_jwt_token(token: str):
    try:
        header = jwt.get_unverified_header(token)
        key = next(k for k in jwks['keys'] if k['kid'] == header['kid'])

        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=settings.cognito_client_id,
            issuer=f"https://cognito-idp.{settings.aws_region}.amazonaws.com/{settings.cognito_user_pool_id}"
        )
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid or expired token: {e}")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    return decode_jwt_token(token)
