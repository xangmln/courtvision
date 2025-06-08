from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from app.model.abstract import AbstractBaseModel

class Court(AbstractBaseModel):
    __tablename__ = 'court'
    name : Mapped[str] = mapped_column(unique=True)
    location : Mapped[str] = mapped_column(nullable=False)
    

    timeslots = relationship("Timeslot", back_populates="court")
    
    def __str__(self) -> str:
        return self.name