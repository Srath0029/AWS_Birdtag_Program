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

    def login_user(self, username: str, password: str):
        try:
            response = self.client.initiate_auth(
                ClientId=settings.cognito_client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    "USERNAME": username,
                    "PASSWORD": password,
                    "SECRET_HASH": self._get_secret_hash(username)
                }
            )
            return {
                "access_token": response["AuthenticationResult"]["AccessToken"],
                "id_token": response["AuthenticationResult"]["IdToken"],
                "refresh_token": response["AuthenticationResult"]["RefreshToken"],
                "token_type": response["AuthenticationResult"]["TokenType"],
                "expires_in": response["AuthenticationResult"]["ExpiresIn"]
            }
        except ClientError as e:
            raise Exception(e.response["Error"]["Message"])

    def confirm_user(self, username: str, code: str):
        try:
            response = self.client.confirm_sign_up(
                ClientId=settings.cognito_client_id,
                Username=username,
                ConfirmationCode=code,
                SecretHash=self._get_secret_hash(username)
            )
            return {"message": "User confirmed successfully."}
        except ClientError as e:
            raise Exception(e.response["Error"]["Message"])


cognito_service = CognitoService()
