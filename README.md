# VisionMate Navigation Assistant

VisionMate is an AI-powered navigation assistant designed specifically for visually impaired individuals. It uses computer vision and real-time object detection to help users navigate their surroundings safely.

## Features

- Real-time object detection
- Distance estimation
- Directional information (left, center, right)
- Priority-based audio announcements
- Continuous scanning of surroundings
- Urgent warnings for nearby obstacles

## Tech Stack

- Frontend: React + TypeScript + Vite
- Backend: FastAPI + Python
- Object Detection: YOLOv8
- Text-to-Speech: gTTS

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Ani12234/blind.git
cd blind
```

2. Install frontend dependencies:
```bash
cd frontend-new
npm install
```

3. Install backend dependencies:
```bash
cd ../backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running the Application

1. Start the backend server:
```bash
cd backend
uvicorn main:app --reload
```

2. Start the frontend development server:
```bash
cd frontend-new
npm run dev
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Deployment

The application is deployed on Vercel:
- Production URL: [Your Vercel URL]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
