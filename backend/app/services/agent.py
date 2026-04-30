from app.config import settings
from typing import List, Dict
from app.models import Message


class AgentService:
    """Service for managing agent personality and logic"""
    
    def __init__(self):
        self.name = settings.AGENT_NAME
        self.personality = settings.AGENT_PERSONALITY
        self.background = settings.AGENT_BACKGROUND
    
    def get_system_prompt(self) -> str:
        """Generate system prompt with agent personality"""
        return settings.CHAT_SYSTEM_PROMPT_TEMPLATE.format(
            agent_name=self.name,
            personality=self.personality,
            background=self.background
        )
    
    def format_conversation_history(self, messages: List[Message]) -> List[Dict]:
        """Format conversation history for OpenAI API"""
        formatted = []
        for msg in messages:
            formatted.append({
                "role": msg.role,
                "content": msg.content
            })
        return formatted
    
    def get_agent_info(self) -> Dict:
        """Return agent information"""
        return {
            "name": self.name,
            "personality": self.personality,
            "background": self.background
        }
    
    def should_respond_verbosely(self, message: str) -> bool:
        """Determine if agent should give detailed response"""
        verbose_keywords = ["explain", "tell me more", "elaborate", "details", "how", "why"]
        return any(keyword in message.lower() for keyword in verbose_keywords)


agent_service = AgentService()
