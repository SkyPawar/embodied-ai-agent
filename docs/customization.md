# Customization Guide

## Customize Agent Personality

Edit the agent properties in your `.env` file:

```env
AGENT_NAME=Luna
AGENT_PERSONALITY=friendly, helpful, wise, mature, empathetic
AGENT_BACKGROUND=I'm an AI assistant designed to have genuine conversations...
```

Or modify them in `backend/app/services/agent.py`:

```python
def __init__(self):
    self.name = "Luna"
    self.personality = "friendly, helpful, wise, mature, empathetic"
    self.background = "Your background story here..."
```

## Modify System Prompt

Edit `CHAT_SYSTEM_PROMPT_TEMPLATE` in `backend/app/config.py`:

```python
CHAT_SYSTEM_PROMPT_TEMPLATE: str = (
    "You are {agent_name}, a personable and intelligent AI assistant. "
    "Your personality traits: {personality}. "
    "Background: {background}. "
    "[Add your custom instructions here]"
)
```

## Change LLM Model

Modify in `.env`:

```env
OPENAI_MODEL=gpt-4-turbo-preview  # or gpt-3.5-turbo, etc.
```

## Adjust Response Parameters

In `.env`:

```env
OPENAI_TEMPERATURE=0.7        # Lower = more focused, Higher = more creative
OPENAI_MAX_TOKENS=2000        # Max response length
```

## Customize Voice (TTS)

### Change Voice

```env
# Male voices: en-US-Neural2-A, en-US-Neural2-C
# Female voices: en-US-Neural2-C, en-US-Neural2-E
TTS_VOICE_NAME=en-US-Neural2-C
```

### Adjust Speech Rate

```env
TTS_SPEAKING_RATE=1.0    # 0.25 to 4.0
```

### Adjust Pitch

```env
TTS_PITCH=0.0    # -20.0 to 20.0
```

## Load Custom 3D Models

### 1. Prepare Your Model

Supported formats: `.gltf`, `.glb`, `.obj`, `.fbx` (with conversion)

### 2. Update Avatar Component

Edit `frontend/src/components/Avatar.jsx`:

```javascript
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'

const createPlaceholderAvatar = (scene) => {
  const loader = new GLTFLoader()
  loader.load(
    'models/your-model.glb',
    (gltf) => {
      const model = gltf.scene
      scene.add(model)
      // Add animations
    }
  )
}
```

## Add Animations

### Idle Animation

```javascript
const idleAnimation = () => {
  avatar.position.y += Math.sin(Date.now() * 0.001) * 0.01
}
```

### Talk Animation

```javascript
const talkAnimation = () => {
  avatar.rotation.x += 0.02
  // Jaw movement, lip sync, etc.
}
```

## Customize Frontend Appearance

### Colors

Edit `frontend/src/index.css`:

```css
:root {
  --primary-color: #6366f1;
  --secondary-color: #ec4899;
  --background-dark: #0f172a;
  --text-light: #f1f5f9;
}
```

### Layout

Edit `frontend/src/App.css` to change:
- Container layout
- Responsive breakpoints
- Gap and padding

## Add Database Support

Replace in-memory storage in `backend/app/routes/chat.py`:

```python
# Current: conversations = {}

# Replace with database:
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///conversations.db')
Session = sessionmaker(bind=engine)
```

## Add User Authentication

```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

@router.post("/message")
async def chat_message(request: ConversationRequest, credentials: HTTPAuthCredentials = Depends(security)):
    # Verify token
    user_id = verify_token(credentials.credentials)
```

## Production Configuration

### Deployment Checklist

- [ ] Set `DEBUG=false`
- [ ] Update `CORS_ORIGINS` with production domain
- [ ] Add authentication/authorization
- [ ] Setup database
- [ ] Configure logging
- [ ] Add rate limiting
- [ ] Setup monitoring
- [ ] Use HTTPS
- [ ] Configure error tracking (e.g., Sentry)

### Environment Variables for Production

```env
DEBUG=false
CORS_ORIGINS=["https://yourdomain.com"]
OPENAI_TEMPERATURE=0.5
MAX_CONVERSATION_HISTORY=100
```
