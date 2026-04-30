from google.cloud import texttospeech
from google.oauth2 import service_account
from app.config import settings
import logging
import json
import os
from io import BytesIO

logger = logging.getLogger(__name__)


class TTSService:
    """Service for Text-to-Speech using Google Cloud"""
    
    def __init__(self):
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Google Cloud TTS client"""
        try:
            credentials_path = settings.GOOGLE_TTS_CREDENTIALS
            
            if credentials_path and os.path.exists(credentials_path):
                credentials = service_account.Credentials.from_service_account_file(
                    credentials_path
                )
                self.client = texttospeech.TextToSpeechClient(credentials=credentials)
            else:
                # Use default credentials if available
                self.client = texttospeech.TextToSpeechClient()
            
            logger.info("Google Cloud TTS client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize TTS client: {str(e)}")
            self.client = None
    
    async def text_to_speech(self, text: str) -> bytes:
        """Convert text to speech
        
        Args:
            text: Text to convert to speech
        
        Returns:
            Audio bytes (MP3)
        """
        if not self.client:
            logger.warning("TTS client not initialized")
            return b""
        
        try:
            input_text = texttospeech.SynthesisInput(text=text)
            
            voice = texttospeech.VoiceSelectionParams(
                language_code=settings.TTS_LANGUAGE_CODE,
                name=settings.TTS_VOICE_NAME
            )
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=settings.TTS_SPEAKING_RATE,
                pitch=settings.TTS_PITCH
            )
            
            response = self.client.synthesize_speech(
                input=input_text,
                voice=voice,
                audio_config=audio_config
            )
            
            return response.audio_content
        
        except Exception as e:
            logger.error(f"TTS error: {str(e)}")
            return b""


tts_service = TTSService()
