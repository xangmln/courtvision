from __future__ import annotations


from typing import Annotated
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt,JWTError
from sqlalchemy.orm import Session
import os


from app.model.user import User
from app.model.access_token import AccessToken
from app.model.notification import Notification
from app.utils.dependencies import get_db
from app.schemas.user import UserCreate, UserLogin
from app.schemas.token import Token



bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
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
        db.refresh()

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


    def hashed_password(self, password: str) -> str:
        return bcrypt_context.hash(password)
    
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
    
    def delete_user(self, db : db_dependency, user_id : str):
        user_delete = db.query(User).filter(User.id==user_id).first()
        if not user_delete:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            ) 
        db.delete(user_delete)
        db.commit()
        return {"message" : "User Deleted"}

user_service = UserService()