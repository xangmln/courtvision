from fastapi import APIRouter
from app.routers.auth import auth

route = APIRouter()

route.include_router(auth)