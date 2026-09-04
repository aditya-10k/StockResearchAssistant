import time
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def healthcheck():
    return {
        "status": "ok",
        "service": "Stock Research Assistant API",
        "timestamp": int(time.time()),
    }