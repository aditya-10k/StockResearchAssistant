from fastapi import APIRouter

from app.api.routes.health import router as health
from app.api.routes.query import router as query
from app.api.routes.chats import router as chats

main_router = APIRouter()

main_router.include_router(health)
main_router.include_router(query)
main_router.include_router(chats)