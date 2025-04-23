import speech_recognition as sr
from gtts import gTTS
import io
import os
from typing import Optional, Tuple
import logging

class SpeechProcessor:
    def __init__(self, language: str = "en"):
        """
        Initialize the speech processor.
        
        Args:
            language: Default language for speech recognition and synthesis
        """
        self.recognizer = sr.Recognizer()
        self.language = language
        self.logger = logging.getLogger(__name__)
        
    def process_voice_command(self, audio_data: bytes, language: Optional[str] = None) -> Tuple[str, bool]:
        """
        Process voice command from audio data.
        
        Args:
            audio_data: Raw audio data in bytes
            language: Language code for speech recognition (optional)
            
        Returns:
            Tuple of (recognized text, success flag)
        """
        try:
            with sr.AudioFile(io.BytesIO(audio_data)) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(
                    audio,
                    language=language or self.language
                )
                return text, True
        except sr.UnknownValueError:
            self.logger.warning("Speech recognition could not understand audio")
            return "", False
        except sr.RequestError as e:
            self.logger.error(f"Could not request results from speech recognition service: {e}")
            return "", False
        except Exception as e:
            self.logger.error(f"Error processing voice command: {e}")
            return "", False
    
    def text_to_speech(self, text: str, language: Optional[str] = None) -> bytes:
        """
        Convert text to speech audio.
        
        Args:
            text: Text to convert to speech
            language: Language code for speech synthesis (optional)
            
        Returns:
            Audio data in bytes
        """
        try:
            tts = gTTS(text=text, lang=language or self.language)
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            return audio_bytes.read()
        except Exception as e:
            self.logger.error(f"Error converting text to speech: {e}")
            return b""
    
    def is_navigation_command(self, text: str) -> bool:
        """
        Check if the recognized text is a navigation-related command.
        
        Args:
            text: Recognized text from speech
            
        Returns:
            True if the text contains navigation-related keywords
        """
        navigation_keywords = [
            "what", "nearby", "around", "surroundings",
            "detect", "find", "locate", "where"
        ]
        text = text.lower()
        return any(keyword in text for keyword in navigation_keywords)
    
    def generate_navigation_response(self, objects: list) -> str:
        """
        Generate a natural language response about detected objects.
        
        Args:
            objects: List of detected objects and their properties
            
        Returns:
            Natural language response string
        """
        if not objects:
            return "I don't detect any objects nearby."
        
        response = "I detect "
        if len(objects) == 1:
            response += objects[0]
        else:
            response += ", ".join(objects[:-1]) + " and " + objects[-1]
        
        response += " nearby."
        return response 