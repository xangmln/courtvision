from pydantic import BaseModel, Field


class CourtBase(BaseModel):
    courtname : str = Field(min_length=1, max_length=20)
    location : str

class CourtResponse(CourtBase):
    timeslot : str