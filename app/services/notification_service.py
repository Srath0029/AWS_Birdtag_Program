import boto3
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# === SNS SETUP ===
sns = boto3.client(
    'sns',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

# === DYNAMODB SETUP ===+
dynamodb = boto3.client(
    'dynamodb',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

TABLE_NAME = "BirdDetections"

# === SNS TOPIC MAPPING ===
def create_or_get_topic(tag):
    topic_arns = {
        "sparrow": "arn:aws:sns:ap-southeast-2:399404566071:birdtag-sparrow",
        "pigeon": "arn:aws:sns:ap-southeast-2:399404566071:birdtag-pigeon",
        "crow": "arn:aws:sns:ap-southeast-2:399404566071:birdtag-crow",
        "kingFisher": "arn:aws:sns:ap-southeast-2:399404566071:birdtag-kingfisher"
    }
    return topic_arns.get(tag.lower())

# === SAVE TO DYNAMODB ===
def store_tagged_file(source_path, file_type, file_url, tag_counts, thumbnail_url=None):
    dynamo_item = {
        "source_path": {"S": source_path},
        "timestamp": {"S": datetime.utcnow().isoformat()},
        "file_type": {"S": file_type},
        "file_url": {"S": file_url},
        "tags": {
            "M": {tag: {"N": str(count)} for tag, count in tag_counts.items()}
        }
    }

    if thumbnail_url:
        dynamo_item["thumbnail_url"] = {"S": thumbnail_url}

    print("[DEBUG] Final DynamoDB Entry:\n", dynamo_item)

    response = dynamodb.put_item(
        TableName=TABLE_NAME,
        Item=dynamo_item
    )

    print("✅ Stored to DynamoDB.")
    return response

# === NOTIFY + STORE ===
def notify_tag_subscribers(tag_counts, file_url, source_path, file_type="image", thumbnail_url=None):
    # Save metadata to DynamoDB
    store_tagged_file(
        source_path=source_path,
        file_type=file_type,
        file_url=file_url,
        tag_counts=tag_counts,
        thumbnail_url=thumbnail_url
    )

    # Notify subscribers for each tag
    for tag, count in tag_counts.items():
        topic_arn = create_or_get_topic(tag)
        if topic_arn:
            message = f"A new media file containing {count} '{tag}' was uploaded: {file_url}"
            print(f"📤 Notifying [{tag}] via {topic_arn}")
            sns.publish(
                TopicArn=topic_arn,
                Message=message,
                Subject=f"[BirdTag] {tag} Alert"
            )
