from typing import Annotated
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt,JWTError
from sqlalchemy.orm import Session
import os

from app.model.user import User
from app.model.access_token import AccessToken
from app.utils.dependencies import get_db
from app.schemas.user import UserCreate, UserLogin
from app.schemas.token import Token



bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))

db_dependency = Annotated[Session,get_db()]
class UserService:
    def create_user(self, user: UserCreate, db : Session):
        # 이미 등록된 계정인지 확인
        if self.exists(user.email,db):
            raise HTTPException(status.HTTP_400_BAD_REQUEST,"User with email already exist")
        
        hashed_password = self.hashed_password(user.password)
        user.password = hashed_password
        user = User(**user.model_dump())
        db.add(user)
        db.commit()
        db.refresh()

        token, expiry = self.create_access_token(db,user).values()

        user = json

    def hashed_password(self, password: str) -> str:
        return bcrypt_context.hash(password)
    
    def exists(self, email: str, db: Session) -> bool:
        user = db.query(User).filter(User.email == email).first()

        if user:
            return True

        return False


    def authentication_user(self, email: str, password: str, db):
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return False
        if not bcrypt_context.verify(password, user.password):
            return False
        return user

    def create_access_token(self, db : Session, user : User) -> dict:
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

    def get_current_user(self, token: Annotated[str, Depends(oauth2_bearer)]):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get('sub')
            user_id: int = payload.get('id')
            user_role: str = payload.get('role')
            if email is None or user_id is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail='Could not validate user.')
            return {'email': email, 'id': user_id, 'user_role': user_role}
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')

user_service = UserService()