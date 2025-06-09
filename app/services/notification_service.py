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

# === DYNAMODB SETUP ===
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

table = dynamodb.Table('BirdTagMedia')  # Change to our actual table name

# === TOPIC ARNs ===
def create_or_get_topic(tag):
    topic_arns = {
        "Sparrow": "arn:aws:sns:ap-southeast-2:399404566071:birdtag-sparrow",
        "Pigeon": "arn:aws:sns:ap-southeast-2:399404566071:birdtag-pigeon",
        "Crow": "arn:aws:sns:ap-southeast-2:399404566071:birdtag-crow"
    }
    return topic_arns.get(tag)

# === STORE TO DB ===
def store_tagged_file(file_id, file_type, s3_url, tag_counts):
    item = {
        'file_id': file_id,
        'file_type': file_type,
        's3_url': s3_url,
        'tags': {k: v for k, v in tag_counts.items() if v > 0},
        'timestamp': datetime.utcnow().isoformat()
    }

    response = table.put_item(Item=item)
    print("✅ Stored to DynamoDB:", response)

# === SNS PUBLISHER ===
def notify_tag_subscribers(tag_counts, file_url, file_id="unknown", file_type="video"):
    # First, save metadata to the DB
    store_tagged_file(file_id, file_type, file_url, tag_counts)

    # Then notify subscribers
    for tag, count in tag_counts.items():
        topic_arn = create_or_get_topic(tag)
        if topic_arn:
            message = f"A new media file containing {count} '{tag}' was uploaded: {file_url}"
            print("📤 Notifying topic:", topic_arn)
            sns.publish(
                TopicArn=topic_arn,
                Message=message,
                Subject=f"[BirdTag] {tag} Alert"
            )

    





