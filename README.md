# 🎵 VibeCheck - Emotion-Based Music Recommendation System

A full-stack cloud application that leverages AWS AI services to detect user emotions and recommend personalized music tracks.

![VibeCheck Banner](https://img.shields.io/badge/VibeCheck-Emotion%20Music-blue?style=for-the-badge)
![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=flat-square&logo=react&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?style=flat-square&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)

---

## ✨ Features

| Feature | Description | AWS Service |
|---------|-------------|-------------|
| **Text Emotion Detection** | Analyze mood from written text | Amazon Comprehend |
| **Image Emotion Detection** | Detect facial emotions from selfies | Amazon Rekognition |
| **Smart Music Matching** | Match detected emotion to curated playlists | DynamoDB + Lambda |
| **Secure Streaming** | Private S3 music streaming via pre-signed URLs | Amazon S3 |
| **Premium UI** | Glassmorphism design with dynamic themes | React + Vite |
| **History Tracking** | Track recent vibe checks per user | DynamoDB |

---

## 🏗️ Architecture

```
┌─────────────────┐      POST /analyze      ┌─────────────────┐
│  React Frontend │ ──────────────────────> │  API Gateway    │
└─────────────────┘                         └────────┬────────┘
      ^                                              │
      │ Pre-signed URLs                              v
      │                                       ┌─────────────────┐
      │                                       │  AWS Lambda     │
      │                                       └────────┬────────┘
      │                                                │
      │         ┌──────────────┬──────────────┬────────┘
      │         v              v              v
      │   ┌─────────┐   ┌──────────┐   ┌──────────┐
      └───┤  S3     │   │Comprehend│   │Rekognition│
          │(Music)   │   │ (Text)   │   │ (Image)   │
          └─────────┘   └──────────┘   └──────────┘
                              │
                              v
                        ┌──────────┐
                        │ DynamoDB │
                        │(Catalog) │
                        └──────────┘
```

---

## 📁 Project Structure

```
emotion_ccl/
├── backend/
│   ├── lambda_handler.py          # AWS Lambda handler
│   └── mock_backend.py            # Local development fallback
├── frontend/
│   ├── index.html                 # Entry HTML
│   ├── index.css                  # Global styles & glassmorphism
│   ├── package.json               # Frontend dependencies
│   └── src/
│       ├── main.jsx               # React entry point
│       └── App.jsx                # Main application component
├── scripts/
│   ├── generate_metadata.py       # Generate 40 demo music tracks
│   ├── seed_dynamodb.py           # Seed DynamoDB with music catalog
│   └── setup_music.sh             # Automated setup script
├── docs/
│   └── aws_setup_guide.md         # Full AWS deployment guide
├── data/
│   └── music_metadata.json        # Generated music catalog data
└── README.md                      # This file
```

---

## 🚀 Quick Start

### Prerequisites
- [Node.js](https://nodejs.org/) (v16+)
- [Python](https://python.org/) (3.9+)
- [AWS CLI](https://aws.amazon.com/cli/) configured with credentials
- AWS Account with access to Comprehend, Rekognition, DynamoDB, S3, Lambda

### 1. Clone & Setup
```bash
git clone https://github.com/sereenat7/emotion_ccl.git
cd emotion_ccl
```

### 2. Generate Demo Music Data
```bash
python scripts/generate_metadata.py
```
This creates 40 sample tracks across 4 emotions: **Happy, Sad, Angry, Calm**.

### 3. Deploy AWS Backend
Follow the detailed [AWS Setup Guide](./docs/aws_setup_guide.md) to:
1. Create S3 bucket for music storage
2. Set up DynamoDB tables (`MusicCatalog`, `Users`)
3. Deploy Lambda function with IAM roles
4. Configure API Gateway with CORS

### 4. Seed DynamoDB
```bash
python scripts/seed_dynamodb.py
```

### 5. Update API Endpoint
Edit `frontend/src/App.jsx` and replace `API_ENDPOINT` with your API Gateway URL:
```javascript
const API_ENDPOINT = 'https://your-api.execute-api.region.amazonaws.com/prod/analyze';
```

### 6. Run Frontend Locally
```bash
cd frontend
npm install
npm run dev
```
Visit `http://localhost:5173` 🎉

---

## 🎨 UI Preview

The application features a **glassmorphism design** with:
- Dynamic color themes based on detected emotion
- Animated gradient spheres in background
- Smooth hover effects and transitions
- Responsive grid layout

| Emotion | Theme Color |
|---------|-------------|
| Happy | 🟡 Warm Yellow |
| Sad | 🔵 Deep Blue |
| Angry | 🔴 Intense Red |
| Calm | 🟢 Soft Green |

---

## 🔌 API Reference

### `POST /analyze`

Detects emotion and returns music recommendations.

**Request Body:**
```json
{
  "type": "text",
  "data": "I'm feeling great today!",
  "userId": "user123"
}
```

**Response:**
```json
{
  "emotion": "HAPPY",
  "songs": [
    {
      "emotion": "HAPPY",
      "songName": "Walking on Sunshine",
      "genre": "Pop",
      "streamUrl": "https://s3.presigned.url/..."
    }
  ]
}
```

**Supported Input Types:**
- `text` - Analyzes sentiment via Amazon Comprehend
- `image` - Base64-encoded image for facial analysis via Amazon Rekognition

---

## 🔒 Security

- **IAM Roles** for cross-service authentication (no hardcoded AWS keys)
- **S3 Pre-signed URLs** for secure, time-limited music access
- **CORS Configuration** for controlled API access
- **Private S3 Buckets** with no public access

---

## 🛠️ Technologies Used

### Frontend
- React 18
- Vite (build tool)
- CSS3 with Glassmorphism effects

### Backend
- Python 3.9+
- AWS Lambda
- Boto3 (AWS SDK)

### AWS Services
- Amazon Comprehend (NLP sentiment analysis)
- Amazon Rekognition (facial emotion detection)
- Amazon DynamoDB (NoSQL database)
- Amazon S3 (object storage)
- AWS API Gateway (REST API)
- AWS IAM (access management)

---

## 📝 Scripts Reference

| Script | Purpose |
|--------|---------|
| `generate_metadata.py` | Creates 40 demo music entries with SoundHelix URLs |
| `seed_dynamodb.py` | Creates DynamoDB tables and populates with music data |
| `setup_music.sh` | Automated environment setup (Linux/Mac) |

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 👥 Team

| Name | Role |
|------|------|
| Sereenat7 | Project Lead & Backend |
| Aditi Tarase | Frontend & UI Design |

---

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2025 VibeCheck Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- Demo music tracks powered by [SoundHelix](https://www.soundhelix.com)
- AWS Free Tier for cloud infrastructure
- React & Vite communities for exce