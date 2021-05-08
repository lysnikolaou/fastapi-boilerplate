from fastapi import APIRouter

from rook.api.endpoints import health

router = APIRouter()

router.include_router(health.router, tags=["health"])
