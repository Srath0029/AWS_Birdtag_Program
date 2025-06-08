import boto3
import os
from dotenv import load_dotenv
load_dotenv()


sns = boto3.client(
    'sns',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

def create_or_get_topic(tag):
    topic_arns = {
        "Sparrow": "arn:aws:sns:ap-southeast-2:399404566071:birdtag-sparrow"
        # You can add more topics here later if needed
    }
    return topic_arns.get(tag)


def notify_tag_subscribers(tag_counts, file_url):
    for tag, count in tag_counts.items():
        topic_arn = create_or_get_topic(tag)
        message = f"A new media file containing {count} '{tag}' was uploaded: {file_url}"
        sns.publish(TopicArn=topic_arn, Message=message, Subject=f"[BirdTag] {tag} Alert")

def create_or_get_topic(tag):
    return "arn:aws:sns:ap-southeast-2:399404566071:birdtag-sparrow"

def notify_tag_subscribers(tag_counts, file_url):
    for tag, count in tag_counts.items():
        topic_arn = create_or_get_topic(tag)
        message = f"A new media file containing {count} '{tag}' was uploaded: {file_url}"
        print("🔔 SENDING:", message)
        sns.publish(
            TopicArn=topic_arn,
            Subject=f"[BirdTag] {tag} Alert",
            Message=message
        )

