from datetime import datetime

from pydantic import BaseModel, Field, EmailStr
from typing import Literal

from app.model.user import RoleEnum


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length=20)
    email: EmailStr
    role: Literal["user","admin"] = "user"


class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreateResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    access_token: str
    expiry: datetime

class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr