from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # API Configuration
    API_TITLE: str = "Embodied AI Agent"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative frontend port
        "http://localhost:8080",  # Alternative frontend port
    ]
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    OPENAI_MAX_TOKENS: int = int(os.getenv("OPENAI_MAX_TOKENS", "2000"))
    OPENAI_TEMPERATURE: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    
    # Google Cloud TTS Configuration
    GOOGLE_TTS_CREDENTIALS: str = os.getenv("GOOGLE_TTS_CREDENTIALS", "")
    TTS_LANGUAGE_CODE: str = os.getenv("TTS_LANGUAGE_CODE", "en-US")
    TTS_VOICE_NAME: str = os.getenv("TTS_VOICE_NAME", "en-US-Neural2-C")  # Female voice
    TTS_SPEAKING_RATE: float = float(os.getenv("TTS_SPEAKING_RATE", "1.0"))
    TTS_PITCH: float = float(os.getenv("TTS_PITCH", "0.0"))
    
    # Agent Configuration
    AGENT_NAME: str = os.getenv("AGENT_NAME", "Luna")
    AGENT_PERSONALITY: str = os.getenv(
        "AGENT_PERSONALITY",
        "friendly, helpful, wise, mature, empathetic, with a touch of humor"
    )
    AGENT_BACKGROUND: str = os.getenv(
        "AGENT_BACKGROUND",
        "I'm an AI assistant designed to have genuine, warm conversations. "
        "I aim to be helpful while maintaining a natural, human-like communication style."
    )
    
    # Chat Configuration
    CHAT_SYSTEM_PROMPT_TEMPLATE: str = (
        "You are {agent_name}, a personable and intelligent AI assistant. "
        "Your personality traits: {personality}. "
        "Background: {background}. "
        "Communicate naturally as if you were a real person having a conversation. "
        "Be warm, engaging, and genuine in your responses. "
        "Keep responses concise unless asked for more detail."
    )
    
    MAX_CONVERSATION_HISTORY: int = int(os.getenv("MAX_CONVERSATION_HISTORY", "20"))
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
