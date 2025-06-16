from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import Annotated
from sqlalchemy.orm import Session

from app.model.court import Court
from app.schemas.court import CourtBase
from app.utils.dependencies import get_db

db_dependency = Annotated[Session,Depends(get_db)]

class CourtServise:
    async def create_court(self, court : CourtBase, db : db_dependency):
        # 이미 등록된 코트인지 확인
        if self.exists(court.courtname,db):
            raise HTTPException(status.HTTP_400_BAD_REQUEST,"This Court is already exist")
        court = Court(**court.model_dump())
        db.add(court)
        db.close
        db.refresh(court)

        court = jsonable_encoder(
            self.get_court_detail(db=db,court_name=court.name)
        )
        response = {
            "court" : court
        }
        return response


    async def exists(self, name : str, db : db_dependency):
        court = db.query(Court).filter(name == Court.name).first()
        if court:
            return True
        return False
    
    async def get_court_detail(self, db: db_dependency, court_name: str):
        query = db.query(Court).filter(Court.name == court_name).first()
        if not query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            ) 
        return query









court_service = CourtServise()