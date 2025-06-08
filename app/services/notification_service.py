# services/notification_service.py

import boto3
import os

sns = boto3.client(
    'sns',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

def create_or_get_topic(tag):
    topic_name = f'birdtag-{tag.lower()}'
    response = sns.create_topic(Name=topic_name)
    return response['TopicArn']

def notify_tag_subscribers(tag_counts, file_url):
    for tag, count in tag_counts.items():
        topic_arn = create_or_get_topic(tag)
        message = f"A new media file containing {count} '{tag}' was uploaded: {file_url}"
        subject = f"[BirdTag Alert] {tag} detected!"

        sns.publish(
            TopicArn=topic_arn,
            Subject=subject,
            Message=message
        )
