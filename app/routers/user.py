from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated

from app.response.success_response import success_response
from app.utils.dependencies import get_db
from app.service.user import user_service
from app.schemas.user import UserResponse, UserLogin, UserUpdate, UserPassword
from app.model.user import User

user = APIRouter(prefix="/user",tags=["user"])

db_dependency = Annotated[Session,Depends(get_db)]

@user.get("/", summary="Get list of users")
async def get_users(search: str = "", db: Session = Depends(get_db)):
    users = user_service.fetch_all(db=db, search=search)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="User list fetched successfully",
        data=users,
    )



@user.get("/{id}" ,status_code=status.HTTP_200_OK)
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

@user.patch("/{id}", summary="Update user profile")
async def update_user_profile(
    id: str,
    body: UserUpdate,
    user: User = Depends(user_service.get_current_user),
    db: Session = Depends(get_db),
):
    data = user_service.update_user_profile(db=db, user=user, user_id=id, schema=body)

    return success_response(message="User updated successfully", data=data)

@user.patch("/password")
async def change_password(body: UserPassword,user: User= Depends(user_service.get_current_user), db: Session = Depends(get_db)):
    data = user_service.change_password(db,user.email,body.password,body.new_password)

    return success_response(message="User password changed successfully", data=data)
