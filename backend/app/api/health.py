from fastapi import APIRouter

from services.health_service import get_health_status

router = APIRouter()


@router.get("/health")
def health_check():
    return get_health_status()