# app/services/cognito_service.py

import boto3
import hmac
import hashlib
import base64
from app.config.settings import settings

from botocore.exceptions import ClientError
from app.config.settings import settings

class CognitoService:
    def __init__(self):
        self.client = boto3.client("cognito-idp", region_name=settings.aws_region)

    def _get_secret_hash(self, username: str) -> str:
        message = username + settings.cognito_client_id
        digest = hmac.new(
            settings.cognito_client_secret.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256
        ).digest()
        return base64.b64encode(digest).decode()

    def sign_up_user(self, username: str, password: str, email: str):
        try:
            response = self.client.sign_up(
                ClientId=settings.cognito_client_id,
                Username=username,
                Password=password,
                UserAttributes=[
                    {"Name": "email", "Value": email},
                ],
                SecretHash=self._get_secret_hash(username)
            )
            return {"message": "Signup successful. Please verify your email."}
        except ClientError as e:
            raise Exception(e.response["Error"]["Message"])


cognito_service = CognitoService()
