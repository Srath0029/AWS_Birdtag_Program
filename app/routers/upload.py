# app/routers/upload.py

from fastapi import APIRouter, HTTPException
from app.config.settings import settings
from app.models.upload_models import PresignRequest
from app.services.upload_service import generate_presigned_url
import boto3
import uuid
from datetime import datetime
# from app.utils.logger import logger


router = APIRouter()

@router.post("/generate-presigned-url")
def generate_presigned_url(content_type: str):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.aws_region,
    )

    file_extension = content_type.split("/")[-1]
    filename = f"{uuid.uuid4()}.{file_extension}"

    try:
        presigned_url = s3.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": settings.s3_bucket_name,
                "Key": f"uploads/{filename}",
                "ContentType": content_type,
            },
            ExpiresIn=300
        )

        # logger.info("Presigned URL generated successfully", extra={
        #     "module": "upload_service",
        #     "filename": filename,
        #     "content_type": content_type,
        #     "bucket": settings.s3_bucket_name
        # })

        return {
            "upload_url": presigned_url,
            "file_key": f"uploads/{filename}",
            "expires_in": 300
        }

    except Exception as e:
        # logger.error("Failed to generate presigned URL", extra={
        #     "module": "upload_service",
        #     "error": str(e),
        #     "content_type": content_type
        # })
        raise HTTPException(status_code=500, detail=f"Failed to generate presigned URL: {e}")


# @router.post("/generate-url")
# def get_upload_url(payload: PresignRequest):
#     url = generate_presigned_url(payload.filename, payload.content_type)
#     return {"url": url}