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
    data = user_service.create_user(user,db)

    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="User created successfully",
        data=data
    )


@auth.post("/login", status_code=status.HTTP_200_OK)
async def login(data: UserLogin, db: Session = Depends(get_db)):
    data = user_service.handle_login(db, email=data.email, password=data.password)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="User login successful",
        data=data,
    )


@auth.post("/logout")
async def logout(
    current_user: User = Depends(user_service.get_current_user),
    db: Session = Depends(get_db),
):
    user_service.blacklist_token(db, current_user)
    return success_response(message="User logged out successfully")