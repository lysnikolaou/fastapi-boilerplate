from fastapi import APIRouter

from rook.api.endpoints import health, user

router = APIRouter()

router.include_router(health.router, tags=["health"])
router.include_router(user.router, prefix="/users", tags=["user"])
