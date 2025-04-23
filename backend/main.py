from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import cv2
import numpy as np
from ultralytics import YOLO
import speech_recognition as sr
from gtts import gTTS
import os
from geopy.geocoders import Nominatim
import io
import base64
from typing import List, Optional

app = FastAPI(title="VisionMate API")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize YOLO model
model = YOLO('yolov8n.pt')

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Initialize geolocator
geolocator = Nominatim(user_agent="visionmate")

class ObjectDetectionResponse(BaseModel):
    objects: List[str]
    confidence: List[float]
    distances: List[float]

class VoiceCommandResponse(BaseModel):
    text: str
    language: str

@app.post("/detect-objects", response_model=ObjectDetectionResponse)
async def detect_objects(file: UploadFile = File(...)):
    try:
        # Read image file
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Perform object detection
        results = model(img)
        
        # Process results
        objects = []
        confidence = []
        distances = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                objects.append(model.names[cls])
                confidence.append(conf)
                # Estimate distance (placeholder - would need depth camera for accurate measurements)
                distances.append(0.0)
        
        return ObjectDetectionResponse(
            objects=objects,
            confidence=confidence,
            distances=distances
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-voice-command", response_model=VoiceCommandResponse)
async def process_voice_command(file: UploadFile = File(...), language: str = "en"):
    try:
        # Read audio file
        contents = await file.read()
        
        # Process audio with speech recognition
        with sr.AudioFile(io.BytesIO(contents)) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language=language)
        
        return VoiceCommandResponse(text=text, language=language)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/location-context")
async def get_location_context(latitude: float, longitude: float):
    try:
        location = geolocator.reverse(f"{latitude}, {longitude}")
        return {
            "address": location.address,
            "raw": location.raw
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/text-to-speech")
async def text_to_speech(text: str, language: str = "en"):
    try:
        tts = gTTS(text=text, lang=language)
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return {"audio": base64.b64encode(audio_bytes.read()).decode()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 