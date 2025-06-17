from fastapi import APIRouter,Depends,status

from sqlalchemy.orm import Session
from typing import Annotated

from app.utils.dependencies import get_db
from app.schemas.court import CourtBase
from app.service.court import court_service
from app.response.success_response import success_response

db_dependency = Annotated[Session,Depends(get_db)]

court = APIRouter(prefix="/court", tags=["court"])

@court.post("/register",status_code=status.HTTP_201_CREATED)
async def court_register(court : CourtBase ,db : db_dependency):
    data = court_service.create_court(court,db)
    return success_response(
        status_code=status.HTTP_201_CREATED,
        message="Court created successfully",
        data=data
    )

