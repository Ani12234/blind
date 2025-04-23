import { useState, useRef, useEffect } from 'react';
import { 
  Box, 
  Container, 
  Paper, 
  Typography, 
  Snackbar,
  Alert
} from '@mui/material';
import Webcam from 'react-webcam';
import axios from 'axios';

const API_URL = process.env.VITE_API_URL || 'http://localhost:8000';

// Constants for distance estimation
const MIN_DISTANCE = 1; // meters
const MAX_DISTANCE = 10; // meters
const DANGER_DISTANCE = 2; // meters

interface DetectedObject {
  name: string;
  confidence: number;
  distance: number;
  position: 'left' | 'center' | 'right';
}

function App() {
  const [detectedObjects, setDetectedObjects] = useState<DetectedObject[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [lastDetectionTime, setLastDetectionTime] = useState<number>(0);
  const [lastAnnouncementTime, setLastAnnouncementTime] = useState<number>(0);
  const webcamRef = useRef<Webcam>(null);

  // Auto-detect objects every 2 seconds for real-time feedback
  useEffect(() => {
    const interval = setInterval(() => {
      const now = Date.now();
      if (now - lastDetectionTime >= 2000) { // 2 seconds
        detectObjects();
        setLastDetectionTime(now);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [lastDetectionTime]);

  // Auto-announce important objects every 5 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      const now = Date.now();
      if (now - lastAnnouncementTime >= 5000) { // 5 seconds
        announceImportantObjects();
        setLastAnnouncementTime(now);
      }
    }, 5000);

    return () => clearInterval(interval);
  }, [lastAnnouncementTime, detectedObjects]);

  const detectObjects = async () => {
    try {
      setIsLoading(true);
      const imageSrc = webcamRef.current?.getScreenshot();
      if (!imageSrc) {
        throw new Error('Could not capture image');
      }

      // Convert base64 to blob
      const response = await fetch(imageSrc);
      const blob = await response.blob();
      const file = new File([blob], 'photo.jpg', { type: 'image/jpeg' });

      const formData = new FormData();
      formData.append('file', file);

      const result = await axios.post(`${API_URL}/detect-objects`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Process and enhance the detection results
      const enhancedObjects = result.data.objects.map((obj: string, index: number) => {
        const confidence = result.data.confidence[index];
        const distance = result.data.distances[index];
        const position = getObjectPosition(index, result.data.objects.length);
        
        return {
          name: obj,
          confidence,
          distance,
          position
        };
      });

      setDetectedObjects(enhancedObjects);
      
      // Immediately announce critical objects
      announceCriticalObjects(enhancedObjects);
    } catch (err) {
      setError('Error detecting objects: ' + (err as Error).message);
    } finally {
      setIsLoading(false);
    }
  };

  const getObjectPosition = (index: number, total: number): 'left' | 'center' | 'right' => {
    if (total <= 1) return 'center';
    const position = index / (total - 1);
    if (position < 0.33) return 'left';
    if (position > 0.66) return 'right';
    return 'center';
  };

  const announceCriticalObjects = (objects: DetectedObject[]) => {
    const criticalObjects = objects.filter(obj => 
      obj.distance <= DANGER_DISTANCE && obj.confidence > 0.7
    );

    if (criticalObjects.length > 0) {
      const message = criticalObjects.map(obj => 
        `Warning! ${obj.name} ${getDistanceDescription(obj.distance)} ${obj.position}`
      ).join('. ');
      
      speakMessage(message, true); // true for urgent tone
    }
  };

  const announceImportantObjects = () => {
    const importantObjects = detectedObjects.filter(obj => 
      obj.confidence > 0.5 && obj.distance <= MAX_DISTANCE
    );

    if (importantObjects.length > 0) {
      const message = importantObjects.map(obj => 
        `${obj.name} ${getDistanceDescription(obj.distance)} ${obj.position}`
      ).join('. ');
      
      speakMessage(message);
    }
  };

  const getDistanceDescription = (distance: number): string => {
    if (distance <= DANGER_DISTANCE) return 'very close';
    if (distance <= 5) return 'nearby';
    return 'ahead';
  };

  const speakMessage = async (message: string, urgent: boolean = false) => {
    try {
      const response = await axios.post(
        `${API_URL}/text-to-speech?text=${encodeURIComponent(message)}&language=en`
      );

      const audio = new Audio(`data:audio/mp3;base64,${response.data.audio}`);
      if (urgent) {
        audio.playbackRate = 1.2; // Faster speech for urgent messages
      }
      await audio.play();
    } catch (err) {
      setError('Error with text to speech: ' + (err as Error).message);
    }
  };

  return (
    <Container maxWidth="md" role="main" aria-label="VisionMate - Navigation Assistant">
      <Box sx={{ my: 4 }}>
        <Typography 
          variant="h4" 
          component="h1" 
          gutterBottom
          role="heading"
          aria-level={1}
        >
          VisionMate Navigation Assistant
        </Typography>
        
        <Paper 
          elevation={3} 
          sx={{ p: 2, mb: 2 }}
          role="region"
          aria-label="Camera feed"
        >
          <Webcam
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            style={{ width: '100%', height: 'auto' }}
            aria-hidden="true"
          />
        </Paper>

        {isLoading && (
          <Typography 
            role="status"
            aria-live="polite"
          >
            Scanning surroundings...
          </Typography>
        )}

        {detectedObjects.length > 0 && (
          <Paper 
            elevation={3} 
            sx={{ p: 2 }}
            role="region"
            aria-label="Detected objects"
          >
            <Typography 
              variant="h6" 
              gutterBottom
              role="heading"
              aria-level={2}
            >
              Surroundings:
            </Typography>
            <ul role="list">
              {detectedObjects.map((obj, index) => (
                <li key={index} role="listitem">
                  {obj.name} - {getDistanceDescription(obj.distance)} - {obj.position}
                </li>
              ))}
            </ul>
          </Paper>
        )}

        <Snackbar
          open={!!error}
          autoHideDuration={6000}
          onClose={() => setError(null)}
          role="alert"
        >
          <Alert 
            onClose={() => setError(null)} 
            severity="error"
            role="alert"
          >
            {error}
          </Alert>
        </Snackbar>
      </Box>
    </Container>
  );
}

export default App; 