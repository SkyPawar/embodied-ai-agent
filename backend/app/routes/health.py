from fastapi import APIRouter
from app.config import settings
from app.models import HealthResponse
from app.services.agent import agent_service

router = APIRouter(prefix="/api/health", tags=["health"])


@router.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version=settings.API_VERSION,
        agent_name=agent_service.name
    )
