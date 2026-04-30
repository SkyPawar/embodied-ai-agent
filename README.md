# 🤖 Embodied AI Agent - Cute & Mature Animated Character

A web-based interactive AI agent with a 3D animated avatar that talks like a real human. Features real-time conversations with personality-driven responses powered by OpenAI's GPT models.

## 🎯 Features

- **3D Animated Avatar** - Beautiful, smooth animations using Three.js
- **Real-time Conversations** - Streaming responses from OpenAI GPT
- **Personality-Driven** - Customizable character traits and personality
- **Text-to-Speech** - Natural voice synthesis (Google Cloud TTS)
- **Speech-to-Text** - Optional user voice input
- **Web-Based** - Fully responsive, browser-based application

## 🏗️ Architecture

```
embodied-ai-agent/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI app entry point
│   │   ├── config.py       # Configuration & settings
│   │   ├── models.py       # Pydantic models
│   │   ├── services/
│   │   │   ├── llm.py      # OpenAI integration
│   │   │   ├── tts.py      # Text-to-Speech service
│   │   │   ├── stt.py      # Speech-to-Text service
│   │   │   └── agent.py    # Agent personality & logic
│   │   └── routes/
│   │       ├── chat.py     # Chat endpoints
│   │       └── health.py   # Health check
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                # React + Three.js frontend
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Avatar.jsx       # 3D avatar component
│   │   │   ├── ChatInterface.jsx # Chat UI
│   │   │   └── VoiceInput.jsx    # Voice recording
│   │   ├── services/
│   │   │   ├── api.js          # API client
│   │   │   └── audioService.js # Audio handling
│   │   ├── models/             # 3D models
│   │   ├── App.jsx
│   │   └── index.css
│   ├── package.json
│   └── .env.example
│
├── docker-compose.yml       # Docker configuration
├── .gitignore
└── docs/                    # Documentation
    ├── setup.md
    ├── api.md
    └── customization.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- OpenAI API Key
- Google Cloud TTS API Key (optional, for voice)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the server
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` in your browser.

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **OpenAI API** - GPT models for conversation
- **Google Cloud TTS** - Natural voice synthesis
- **Pydantic** - Data validation
- **WebSocket** - Real-time streaming

### Frontend
- **React** - UI framework
- **Three.js** - 3D graphics
- **WebGL** - GPU-accelerated rendering
- **Web Audio API** - Audio playback
- **Axios** - HTTP client

## 📋 Environment Variables

### Backend (.env)
```
OPENAI_API_KEY=your_openai_key
GOOGLE_TTS_CREDENTIALS=path/to/credentials.json
AGENT_NAME=Luna
AGENT_PERSONALITY=friendly, helpful, wise
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```

## 🎨 Customization

### Customize Agent Personality
Edit `backend/app/services/agent.py` to define:
- Character name
- Background story
- Personality traits
- Communication style
- Response tone

### Add 3D Models
1. Place your 3D models in `frontend/src/models/`
2. Update `Avatar.jsx` to load your model
3. Define animations in Three.js

## 📚 Documentation

- [Setup Guide](docs/setup.md)
- [API Documentation](docs/api.md)
- [Customization Guide](docs/customization.md)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License - feel free to use this for personal or commercial projects!

## 🎉 Getting Help

- Check the [docs](docs/) folder
- Open an issue on GitHub
- Review example configurations

---

**Happy building! 🚀**