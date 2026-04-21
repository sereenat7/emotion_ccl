# Emotion-Based Music Recommendation System

A full-stack cloud application that leverages AWS AI services to detect user emotions and recommend music.

## Features
- **Emotion Detection (Text)**: Powered by Amazon Comprehend.
- **Emotion Detection (Image)**: Powered by Amazon Rekognition.
- **Music Storage**: Hosted on Amazon S3.
- **Data Management**: DynamoDB for music catalog and user history.
- **Serverless Backend**: AWS Lambda + API Gateway.
- **Premium UI**: Modern React dashboard with glassmorphism design.

## Directory Structure
- `backend/`: Python Lambda source code.
- `frontend/`: React + Vite frontend application.
- `scripts/`: DynamoDB seeding and helper scripts.
- `docs/`: Deployment and setup documentation.

## Quick Start
1. Follow the [AWS Setup Guide](./docs/aws_setup_guide.md).
2. Seed your database using `python3 scripts/seed_dynamodb.py`.
3. Update `frontend/src/App.jsx` with your API URL.
4. Run the frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Security
- Uses **IAM Roles** for cross-service communication (no hardcoded keys).
- Securely streams music via **S3 Pre-signed URLs**.
- CORS configured for secure API access.

## License
MIT
