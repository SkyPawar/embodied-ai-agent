import openai
from app.config import settings
from typing import List, Dict, AsyncGenerator
from app.models import Message
import logging

logger = logging.getLogger(__name__)


class LLMService:
    """Service for OpenAI API interactions"""
    
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.max_tokens = settings.OPENAI_MAX_TOKENS
        self.temperature = settings.OPENAI_TEMPERATURE
    
    async def get_response(
        self,
        messages: List[Dict],
        system_prompt: str,
        stream: bool = False
    ) -> str | AsyncGenerator:
        """Get response from OpenAI API
        
        Args:
            messages: List of message dicts with role and content
            system_prompt: System prompt for the agent
            stream: Whether to stream response
        
        Returns:
            Response text or async generator for streaming
        """
        try:
            formatted_messages = [{"role": "system", "content": system_prompt}] + messages
            
            if stream:
                return await self._stream_response(formatted_messages)
            else:
                return await self._get_full_response(formatted_messages)
        
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
    
    async def _get_full_response(self, messages: List[Dict]) -> str:
        """Get full response (non-streaming)"""
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        return response.choices[0].message.content
    
    async def _stream_response(self, messages: List[Dict]) -> AsyncGenerator:
        """Stream response from OpenAI"""
        stream = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            stream=True
        )
        
        for chunk in stream:
            if "content" in chunk.choices[0].delta:
                yield chunk.choices[0].delta.content


llm_service = LLMService()
