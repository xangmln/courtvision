from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated

from app.response.success_response import success_response
from app.utils.dependencies import get_db
from app.service.user import user_service
from app.schemas.user import UserResponse, UserLogin
from app.model.user import User

user = APIRouter(prefix="/user",tags=["user"])

db_dependency = Annotated[Session,Depends(get_db)]

@user.get("/" ,status_code=status.HTTP_200_OK)
async def get_user_profile(
    user: User = Depends(user_service.get_current_user),
    db: Session = Depends(get_db),
):
    data = user_service.get_user_detail(db=db, user_id=user.id)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="User detail fetched successfully",
        data=data
    )

@user.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id : str,user: User = Depends(user_service.get_current_user), db : Session = Depends(get_db)):
    user_service.delete_user_profile(db,user,id)

    return success_response(status_code=204, message="User deleted successfully")