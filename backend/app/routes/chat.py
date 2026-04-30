from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from app.models import ConversationRequest, ConversationResponse, AgentInfo
from app.services.agent import agent_service
from app.services.llm import llm_service
from app.services.tts import tts_service
from datetime import datetime
import json
import base64
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chat", tags=["chat"])

# In-memory conversation storage (use database in production)
conversations = {}


@router.post("/message", response_model=ConversationResponse)
async def chat_message(request: ConversationRequest):
    """Send a message and get response from agent"""
    try:
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Get or initialize conversation
        if conversation_id not in conversations:
            conversations[conversation_id] = []
        
        messages = conversations[conversation_id]
        
        # Add user message
        messages.append({
            "role": "user",
            "content": request.user_message
        })
        
        # Keep conversation history size manageable
        if len(messages) > 20:
            messages = messages[-20:]
        
        # Get system prompt
        system_prompt = agent_service.get_system_prompt()
        
        # Get response from LLM
        assistant_response = await llm_service.get_response(
            messages=messages,
            system_prompt=system_prompt,
            stream=False
        )
        
        # Add assistant message to history
        messages.append({
            "role": "assistant",
            "content": assistant_response
        })
        
        # Generate TTS audio if requested
        audio_base64 = None
        if request.include_tts:
            audio_bytes = await tts_service.text_to_speech(assistant_response)
            if audio_bytes:
                audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        return ConversationResponse(
            conversation_id=conversation_id,
            assistant_message=assistant_response,
            audio_base64=audio_base64,
            timestamp=datetime.now()
        )
    
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/agent-info", response_model=AgentInfo)
async def get_agent_info():
    """Get agent information"""
    info = agent_service.get_agent_info()
    return AgentInfo(
        name=info["name"],
        personality=info["personality"],
        background=info["background"]
    )


@router.post("/stream")
async def stream_chat(request: ConversationRequest):
    """Stream chat response in real-time"""
    async def generate():
        try:
            conversation_id = request.conversation_id or str(uuid.uuid4())
            
            if conversation_id not in conversations:
                conversations[conversation_id] = []
            
            messages = conversations[conversation_id]
            
            # Add user message
            messages.append({
                "role": "user",
                "content": request.user_message
            })
            
            system_prompt = agent_service.get_system_prompt()
            
            # Stream response
            full_response = ""
            async for chunk in await llm_service.get_response(
                messages=messages,
                system_prompt=system_prompt,
                stream=True
            ):
                full_response += chunk
                yield f"data: {json.dumps({'type': 'text', 'content': chunk})}\n\n"
            
            # Add to conversation history
            messages.append({
                "role": "assistant",
                "content": full_response
            })
            
            # Generate TTS if requested
            if request.include_tts:
                audio_bytes = await tts_service.text_to_speech(full_response)
                if audio_bytes:
                    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
                    yield f"data: {json.dumps({'type': 'audio', 'content': audio_base64})}\n\n"
            
            yield f"data: {json.dumps({'type': 'end', 'conversation_id': conversation_id})}\n\n"
        
        except Exception as e:
            logger.error(f"Stream error: {str(e)}")
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )


@router.delete("/conversation/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    if conversation_id in conversations:
        del conversations[conversation_id]
        return {"status": "deleted", "conversation_id": conversation_id}
    raise HTTPException(status_code=404, detail="Conversation not found")
