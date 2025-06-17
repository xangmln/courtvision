from __future__ import annotations

import os
from dotenv import load_dotenv
from typing import Annotated
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt,JWTError
from sqlalchemy import or_, text
from sqlalchemy.orm import Session

load_dotenv()

from app.model.user import User
from app.model.access_token import AccessToken
from app.model.notification import Notification
from app.utils.dependencies import get_db
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.token import Token



bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/login')
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES","30"))

db_dependency = Annotated[Session,Depends(get_db)]
class UserService:
    def create_user(self, user: UserCreate, db : db_dependency):
        # 이미 등록된 계정인지 확인
        if self.exists(user.email,db):
            raise HTTPException(status.HTTP_400_BAD_REQUEST,"User with email already exist")
        
        hashed_password = self.hashed_password(user.password)
        user.password = hashed_password
        user = User(**user.model_dump())
        db.add(user)
        db.commit()
        db.refresh(user)

        notification = Notification(
            user_id=user.id, message="Account created successfully"
        )

        db.add(notification)
        db.commit()

        token, expiry = self.create_access_token(db,user).values()

        user = jsonable_encoder(
            self.get_user_detail(db=db, user_id=user.id), exclude={"password"}
        )

        response = {
            "access_token": token,
            "expiry": expiry,
            "user": user,
        }

        return response
    
    def handle_login(self,db : db_dependency, email: str, password : str):
        user = self.get_user_by_email(db,email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="no account with this email"
            )
        if not self.verify_password(db,password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Incorrect password"
            )
        

        access_token, expiry = self.create_access_token(db, user).values()

        
        db.commit()
        db.refresh(user)

        # create notification

        notification = Notification(user_id=user.id, message="Account Login successful")

        db.add(notification)
        db.commit()

        user = jsonable_encoder(
            self.get_user_detail(db=db, user_id=user.id), exclude={"password"}
        )

        response = {
            "access_token": access_token,
            "expiry": expiry,
            "user": user,
        }

        return response


    def hashed_password(self, password: str) -> str:
        return bcrypt_context.hash(password)
    def verify_password(self, db: db_dependency, password: str, hashed_password) -> bool:
        return bcrypt_context.verify(password,hashed_password)

    
    def exists(self, email: str, db: db_dependency) -> bool:
        user = db.query(User).filter(User.email == email).first()

        if user:
            return True

        return False
    
    

    def create_access_token(self, db : db_dependency, user : User) -> dict:
        payload = {
            "id" : user.id,
            "username" : user.username,
            "email" : user.email,
        }
        expire = datetime.now(ZoneInfo("Asia/Seoul"))+timedelta(minutes = 30)
        payload.update({"exp": expire})
        token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

        access_token = AccessToken(user_id=user.id, token=token, expiry_time = expire)
        db.add(access_token)
        db.commit()
        db.refresh(access_token)

        return {"token" : token, "expiry_time" : expire}
    
    def get_current_user(self, token: Annotated[str,Depends(oauth2_bearer)] , db: db_dependency):
        auth_exception = HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid credential"
        )
        try:
            payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
            email : str = payload.get("email")

            if not email:
                raise auth_exception
        except JWTError:
            raise auth_exception
        
        #check blacklist
        access_token = db.query(AccessToken).filter(AccessToken.token == token).first()

        if access_token and access_token.blacklisted:
            raise auth_exception

        user = self.get_user_by_email(email, db)

        if not user:
            raise auth_exception

        return user
    
    def blacklist_token(self,db : db_dependency, user : User) -> None:
        access_token = db.query(AccessToken).filter(AccessToken.user_id==user.id).first()
        
        access_token.blacklisted = True

        db.commit()
        db.refresh(access_token)

        notification = Notification(
            user_id=user.id, message="Account logout successful"
        )

        db.add(notification)
        db.commit()

    
    def get_user_detail(self, db : db_dependency, user_id : str):
        query = db.query(User).filter(User.id==user_id).first()
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            ) 
        return query
        

    def get_user_by_email(self, db: db_dependency, email: str) -> User | None:
        if self.exists(email, db):
            return db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, db: db_dependency, id : str) -> User | None:
        return db.query(User).filter(User.id == id).first() or None
    
    def delete_user_profile(self, db: Session, user: User, user_id: str):
        # check if user is the currently logged in user

        if user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete this user",
            )

        db.delete(user)
        db.commit()
   
    def fetch_all(self, db: Session, search: str = ""):
        query = (
            db.query(User).order_by(text("RANDOM()"))
        )

        if search:
            query = query.filter(
                or_(
                    User.username.icontains(f"%{search}%"),
                    User.email.icontains(f"%{search}%"),
                )
            )

        users = query.all()

        return jsonable_encoder(users, exclude={"password"})
    
    def update_user_profile(self, db: Session,user: User, user_id: str, schema : UserUpdate):
        # verify that user is the one logged in

        if user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to update this user",
            )
        
        data = schema.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)

        notification = Notification(
            user_id=user.id, message="Account updated successfully"
        )

        db.add(notification)
        db.commit()

        # return user detail

        return jsonable_encoder(
            self.get_user_detail(db=db, user_id=user_id), exclude={"password"}
        )


user_service = UserService()