### 📩 Tag-Based Notification

This system uses Amazon SNS to send notifications when media containing specific bird tags is uploaded.

- SNS topics are dynamically created per tag (e.g., `birdtag-sparrow`)
- Subscribers are notified via email when relevant media is detected
- Notifications are triggered after the media is processed and tagged