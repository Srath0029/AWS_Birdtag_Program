import sys
import os

# Add the project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.notification_service import notify_tag_subscribers

# Simulated detection result
tag_counts = {
    "sparrow": 2,
    "kingFisher": 3,
    "birdtag-sparrow": 2
}

file_url = "https://s3.amazonaws.com/birdtag/sample.mp4"
source_path = "uploads/sample.mp4"  # matches what's stored in DynamoDB

# Call the function to notify and store metadata
notify_tag_subscribers(
    tag_counts=tag_counts,
    file_url=file_url,
    source_path=source_path,
    file_type="video",  # or "image", "audio"
    thumbnail_url=None  
)