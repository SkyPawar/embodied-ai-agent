from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Message(BaseModel):
    """Chat message model"""
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: Optional[datetime] = None


class ConversationRequest(BaseModel):
    """Request model for chat endpoint"""
    user_message: str = Field(..., min_length=1, max_length=2000)
    conversation_id: Optional[str] = None
    include_tts: bool = True


class ConversationResponse(BaseModel):
    """Response model for chat endpoint"""
    conversation_id: str
    assistant_message: str
    audio_url: Optional[str] = None
    audio_base64: Optional[str] = None
    timestamp: datetime


class StreamingMessage(BaseModel):
    """Streaming message model"""
    type: str  # 'start', 'text', 'end', 'error'
    content: Optional[str] = None
    audio_chunk: Optional[bytes] = None
    error: Optional[str] = None


class AgentInfo(BaseModel):
    """Agent information model"""
    name: str
    personality: str
    background: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    agent_name: str
