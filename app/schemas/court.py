from pydantic import BaseModel, Field


class Court(BaseModel):
    courtname: str = Field(min_length=1, max_length=20)