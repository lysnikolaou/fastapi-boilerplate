from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from rook.api.deps import get_db
from rook.api.schemas.health import HealthResponse

router = APIRouter()


@router.get("/", response_model=HealthResponse)
async def health(db: Session = Depends(get_db)) -> HealthResponse:
    try:
        db.execute("SELECT 1")
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
    return HealthResponse(message="Health OK")
