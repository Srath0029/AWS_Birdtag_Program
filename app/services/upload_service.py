# app/services/s3_service.py

import boto3
from app.config.settings import settings

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.aws_region
)

def generate_presigned_url(filename: str, content_type: str, expiration: int = 3600):
    return s3_client.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': settings.s3_bucket_name,
            'Key': filename,
            'ContentType': content_type
        },
        ExpiresIn=expiration
    )
