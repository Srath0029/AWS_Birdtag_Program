import sys
import os

# Add the project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.notification_service import notify_tag_subscribers

# Add the parent directory to sys.path so Python can find 'services'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.notification_service import notify_tag_subscribers

# Simulated detection result
tag_counts = {
    "Sparrow": 2,
    "Kingfisher": 3
}

file_url = "https://s3.amazonaws.com/birdtag/sample.mp4"

notify_tag_subscribers(tag_counts, file_url)
