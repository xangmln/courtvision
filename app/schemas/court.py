from pydantic import BaseModel, Field
from typing import List
from uuid import UUID

class CourtBase(BaseModel):
    courtname : str = Field(min_length=1, max_length=20)
    location : str

class CourtResponse(CourtBase):
    timeslot_id : List[UUID]