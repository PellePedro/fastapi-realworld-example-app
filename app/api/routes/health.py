from fastapi import APIRouter

from app.core.config import get_app_settings
from app.models.schemas.health import HealthResponse

router = APIRouter()


@router.get("", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    settings = get_app_settings()
    return HealthResponse(
        status="ok",
        version=settings.version,
        environment=settings.app_env.value,
    )
