# VisionMate

VisionMate is an AI-powered real-time navigation assistant designed to help visually impaired individuals navigate their surroundings safely and independently.

## Project Structure

```
visionmate/
├── frontend/          # React Native mobile app
├── backend/           # FastAPI backend server
└── core/              # Core AI components
```

## Features

- Real-time object and obstacle detection using AI-based computer vision
- Voice command recognition for queries
- Multilingual text-to-speech output
- GPS-based location awareness
- Contextual information about surroundings

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- React Native development environment
- Android Studio / Xcode for mobile development

### Installation

1. Clone the repository
2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

### Running the Application

1. Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. Start the frontend app:
   ```bash
   cd frontend
   npm start
   ```

## Technical Stack

- Frontend: React Native
- Backend: FastAPI
- AI: Python, OpenCV, YOLOv8
- Speech: SpeechRecognition, gTTS
- Location: Geopy, Google Maps API

## License

MIT License 