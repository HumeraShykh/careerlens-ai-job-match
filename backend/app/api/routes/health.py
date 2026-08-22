from fastapi import APIRouter

from app import __version__
from app.db.session import database_status
from app.schemas.common import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    db = database_status()
    status = "ok" if (not db["enabled"] or db["available"]) else "degraded"
    return HealthResponse(status=status, version=__version__, database=db)
