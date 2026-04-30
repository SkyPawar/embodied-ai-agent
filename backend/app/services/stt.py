import speech_recognition as sr
import logging

logger = logging.getLogger(__name__)


class STTService:
    """Service for Speech-to-Text"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    async def speech_to_text(self, audio_file) -> str:
        """Convert speech to text
        
        Args:
            audio_file: Audio file or bytes
        
        Returns:
            Recognized text
        """
        try:
            with sr.AudioFile(audio_file) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data)
                return text
        
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return ""
        except sr.RequestError as e:
            logger.error(f"Speech recognition error: {str(e)}")
            return ""
        except Exception as e:
            logger.error(f"Unexpected STT error: {str(e)}")
            return ""


stt_service = STTService()
