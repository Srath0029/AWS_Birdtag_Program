🐦 AWS BirdTag Program
📄 Overview

AWS BirdTag is a serverless, tag-based media notification system built on Amazon Web Services (AWS).
It automatically detects uploaded bird media, identifies associated tags (e.g., sparrow, eagle), and sends real-time notifications to subscribers using Amazon SNS (Simple Notification Service).

This project demonstrates scalable cloud architecture for automating wildlife media monitoring and environmental data collection — ideal for ecological research, citizen science, and wildlife observation applications.

☁️ Architecture

The system follows an event-driven, serverless architecture using multiple AWS services:

🪣 Amazon S3 – Stores uploaded media files (images/videos).

🧠 AWS Lambda – Processes uploads, performs tag detection, and triggers SNS notifications.

📨 Amazon SNS – Dynamically creates notification topics per bird tag and sends email alerts to subscribers.

🐳 Docker – Provides a containerized environment for local development and deployment.

⚙️ API Gateway – Enables external access to tagging and subscription endpoints.

🔍 Key Features

Dynamic Tag Detection – Automatically identifies bird tags in uploaded media.

Per-Tag Notification Topics – Each detected tag (e.g., birdtag-sparrow) creates its own SNS topic.

Automated Email Alerts – Subscribed users receive email notifications when relevant bird media is uploaded.

Serverless Deployment – Efficiently scales on demand without server management.

Configurable Environment – Easily customizable using the included .env.template file.

🧩 How It Works

Upload Media: A photo or video is uploaded to an S3 bucket.

Trigger Function: An S3 event triggers a Lambda function.

Tag Processing: The function analyzes metadata or AI-generated tags.

SNS Topic Creation: If a tag (e.g., “sparrow”) is detected, an SNS topic birdtag-sparrow is created.

Notification: All subscribers to that topic receive an email alert containing the new media information.

📂 Repository Structure
AWS_Birdtag_Program/
│
├── app/                     # Core application logic
├── tests/                   # Unit and integration tests
├── Dockerfile               # Container setup
├── requirements.txt         # Python dependencies
├── start_server.sh          # Startup script
├── .env.template            # Environment configuration template
└── README.md                # Project documentation

🧠 Technologies Used

AWS Lambda

Amazon S3

Amazon SNS

Docker

Python 3.x

Boto3 (AWS SDK for Python)

🚀 Future Enhancements

🔍 Integrate Rekognition for automated image classification.

📊 Add a web dashboard to visualize upload and tag analytics.

🧠 Use machine learning models for intelligent bird species identification.

🔔 Support multi-channel notifications (SMS, push).

💡 Key Takeaways

Demonstrates event-driven design in AWS.

Showcases scalable, serverless notification systems.

Provides a foundation for environmental and research automation use cases.
