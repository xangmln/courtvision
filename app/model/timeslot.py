from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from app.utils.database import Base
from datetime import date, time
from app.model.abstract import AbstractBaseModel

class Timeslot(AbstractBaseModel):
    __tablename__ = 'timeslot'
    start_time : Mapped[time] = mapped_column(nullable=False)
    end_time : Mapped[time] = mapped_column(nullable=False)
    reservation_date : Mapped[date] = mapped_column(nullable=False)
    court_id : Mapped[str] = mapped_column(ForeignKey('court.id'))
    
    court = relationship('Court', back_populates='timeslots')
    reservation = relationship('Reservation', back_populates='timeslot')