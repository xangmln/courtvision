from fastapi import APIRouter
from app.routers.auth import auth

route = APIRouter(prefix="/courtvision")

route.include_router(auth)