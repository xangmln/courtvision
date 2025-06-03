from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.response.success_response import success_response
from app.utils.dependencies import get_db
from app.service.user import user_service
from app.schemas.user import UserCreate, UserLogin
from app.model.user import User

auth = APIRouter(prefix="/auth", tags = ["auth"])

@auth.post("/register",status_code=status.HTTP_201_CREATED)
async def user_register(user: UserCreate, db : Session = Depends(get_db)):
    data = user_service.