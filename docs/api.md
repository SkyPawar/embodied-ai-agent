# API Documentation

## Base URL

```
http://localhost:8000
```

## Endpoints

### Health Check

#### GET `/api/health/`

Check if the application is running and get agent information.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "agent_name": "Luna"
}
```

### Chat

#### POST `/api/chat/message`

Send a message and get a response from the agent.

**Request Body:**
```json
{
  "user_message": "Hello, how are you?",
  "conversation_id": "optional-uuid",
  "include_tts": true
}
```

**Response:**
```json
{
  "conversation_id": "uuid-string",
  "assistant_message": "Hello! I'm doing well, thank you for asking.",
  "audio_base64": "SUQzBAAAI1NUVEUAAAAVAAAA...",
  "timestamp": "2024-01-10T12:30:45.123456"
}
```

#### GET `/api/chat/agent-info`

Get information about the agent.

**Response:**
```json
{
  "name": "Luna",
  "personality": "friendly, helpful, wise, mature, empathetic",
  "background": "I'm an AI assistant designed to have genuine conversations..."
}
```

#### POST `/api/chat/stream`

Stream responses in real-time using Server-Sent Events.

**Request Body:**
```json
{
  "user_message": "Tell me a story",
  "conversation_id": "optional-uuid",
  "include_tts": true
}
```

**Response (Server-Sent Events):**
```
data: {"type": "text", "content": "Once"}
data: {"type": "text", "content": " upon"}
data: {"type": "text", "content": " a"}
...
data: {"type": "audio", "content": "base64-encoded-audio"}
data: {"type": "end", "conversation_id": "uuid"}
```

#### DELETE `/api/chat/conversation/{conversation_id}`

Delete a conversation and its history.

**Response:**
```json
{
  "status": "deleted",
  "conversation_id": "uuid-string"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Message is too long"
}
```

### 404 Not Found
```json
{
  "detail": "Conversation not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error message"
}
```

## Response Headers

All responses include:
- `Content-Type: application/json`
- `CORS headers` for cross-origin requests

## Rate Limiting

Rate limiting is subject to OpenAI API limits. See https://platform.openai.com/docs/guides/rate-limits for details.

## Authentication

Currently, the API does not require authentication. For production, consider adding API key authentication.
