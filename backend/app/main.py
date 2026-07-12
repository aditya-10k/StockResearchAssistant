from fastapi import FastAPI
from app.schemas.query import QueryReq
from app.api.router import main_router
from app.core.config import settings

app = FastAPI(
    title= settings.APP_NAME,
    version=settings.APP_VER
)

app.include_router(main_router)