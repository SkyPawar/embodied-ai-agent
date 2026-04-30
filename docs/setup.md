# Setup Guide

## Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- npm or yarn
- OpenAI API Key
- Google Cloud TTS API Key (optional)

## Backend Setup

### 1. Clone Repository

```bash
git clone https://github.com/SkyPawar/embodied-ai-agent.git
cd embodied-ai-agent
```

### 2. Create Virtual Environment

```bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

```env
OPENAI_API_KEY=your_openai_key_here
GOOGLE_TTS_CREDENTIALS=/path/to/google-credentials.json
AGENT_NAME=Luna
AGENT_PERSONALITY=friendly, helpful, wise
```

### 5. Get API Keys

#### OpenAI API Key
1. Visit https://platform.openai.com/api-keys
2. Create a new API key
3. Copy and paste it to `.env`

#### Google Cloud TTS (Optional)
1. Visit https://cloud.google.com
2. Create a project
3. Enable Text-to-Speech API
4. Create a service account and download credentials
5. Set `GOOGLE_TTS_CREDENTIALS` to the path of your credentials JSON

### 6. Run Backend

```bash
uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Setup Environment Variables

```bash
cp .env.example .env
```

Edit `.env`:

```env
VITE_API_URL=http://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
```

Frontend will be available at `http://localhost:5173`

## Using Docker (Optional)

```bash
docker-compose up
```

This will start both backend and frontend in containers.

## Testing

### Test Backend Health

```bash
curl http://localhost:8000/api/health/
```

Should return:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "agent_name": "Luna"
}
```

### Test Chat API

```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"user_message": "Hello"}'
```

## Troubleshooting

### OpenAI API Errors
- Check that your API key is valid
- Ensure your OpenAI account has sufficient credits
- Check rate limits

### Google Cloud TTS Issues
- Verify credentials file path is correct
- Ensure service account has TTS permissions
- Check that Text-to-Speech API is enabled

### CORS Errors
- Verify frontend URL is in `CORS_ORIGINS` in `config.py`
- Check that you're accessing from the correct domain/port

### Port Already in Use

```bash
# Backend on different port
uvicorn app.main:app --reload --port 8001

# Frontend on different port
VITE_API_URL=http://localhost:8000 npm run dev -- --port 5174
```
