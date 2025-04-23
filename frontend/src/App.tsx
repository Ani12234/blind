import { useState, useRef } from 'react';
import { 
  Box, 
  Button, 
  Container, 
  Paper, 
  Typography, 
  Snackbar,
  Alert
} from '@mui/material';
import Webcam from 'react-webcam';
import axios from 'axios';

// Add type definitions for browser APIs
declare global {
  interface Window {
    fetch: typeof fetch;
    File: typeof File;
    FormData: typeof FormData;
    Audio: typeof Audio;
  }
}

const API_URL = 'http://localhost:8000';

function App() {
  const [detectedObjects, setDetectedObjects] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const webcamRef = useRef<Webcam>(null);

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

      setDetectedObjects(result.data.objects);
      await speakObjects(result.data.objects);
    } catch (err) {
      setError('Error detecting objects: ' + (err as Error).message);
    } finally {
      setIsLoading(false);
    }
  };

  const speakObjects = async (objects: string[]) => {
    try {
      const text = `I detect ${objects.join(', ')} nearby.`;
      const response = await axios.post(`${API_URL}/text-to-speech`, {
        text,
        language: 'en',
      });

      // Create an audio element and play the response
      const audio = new Audio(`data:audio/mp3;base64,${response.data.audio}`);
      await audio.play();
    } catch (err) {
      setError('Error with text to speech: ' + (err as Error).message);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          VisionMate
        </Typography>
        
        <Paper elevation={3} sx={{ p: 2, mb: 2 }}>
          <Webcam
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            style={{ width: '100%', height: 'auto' }}
          />
        </Paper>

        <Button
          variant="contained"
          color="primary"
          onClick={detectObjects}
          disabled={isLoading}
          fullWidth
          sx={{ mb: 2 }}
        >
          {isLoading ? 'Detecting...' : 'Detect Objects'}
        </Button>

        {detectedObjects.length > 0 && (
          <Paper elevation={3} sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Detected Objects:
            </Typography>
            <ul>
              {detectedObjects.map((obj, index) => (
                <li key={index}>{obj}</li>
              ))}
            </ul>
          </Paper>
        )}

        <Snackbar
          open={!!error}
          autoHideDuration={6000}
          onClose={() => setError(null)}
        >
          <Alert onClose={() => setError(null)} severity="error">
            {error}
          </Alert>
        </Snackbar>
      </Box>
    </Container>
  );
}

export default App; 