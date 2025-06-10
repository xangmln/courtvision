from fastapi import APIRouter
from app.routers.auth import auth
from app.routers.user import user
route = APIRouter()

route.include_router(auth)
route.include_router(user)