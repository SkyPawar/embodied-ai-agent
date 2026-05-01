import os
from typing import List, Dict, AsyncGenerator
from openai import OpenAI
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class LLMService:
    """Voice-first AI companion service (no chat style)"""

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.max_tokens = settings.OPENAI_MAX_TOKENS
        self.temperature = settings.OPENAI_TEMPERATURE

    async def get_response(
        self,
        messages: List[Dict],
        system_prompt: str,
        stream: bool = False
    ) -> str:
        """
        Always returns natural spoken-style response
        """

        try:
            formatted_messages = [
                {"role": "system", "content": system_prompt}
            ] + messages

            response = self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )

            text = response.choices[0].message.content

            # 🔥 IMPORTANT: make response more human-like (voice optimized)
            return self._make_voice_friendly(text)

        except Exception as e:
            logger.error(f"LLM ERROR: {str(e)}")
            return "Hmm... I am here. Can you say that again?"

    def _make_voice_friendly(self, text: str) -> str:
        """
        Convert AI response → natural human speech style
        """
        if not text:
            return ""

        # remove robotic patterns
        text = text.replace("\n", " ")

        # small humanization tweaks
        if not text.endswith((".", "?", "!")):
            text += "."

        return text.strip()


llm_service = LLMService()