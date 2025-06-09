# app/services/s3_service.py

import boto3
from app.config.settings import settings
from services.notification_service import notify_tag_subscribers

# After you get tag_counts and s3_url:
notify_tag_subscribers(tag_counts, s3_url)

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
