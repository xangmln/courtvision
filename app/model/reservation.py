from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey

from app.model.abstract import AbstractBaseModel

from datetime import date

class Reservation(AbstractBaseModel):
    __tablename__ = 'reservation'
    user_id : Mapped[str] = mapped_column(ForeignKey('user.id'))
    timeslot_id : Mapped[str] = mapped_column(ForeignKey('timeslot.id'))
    member : Mapped[str] = mapped_column(default=1)

    user = relationship('User', back_populates='reservations')
    timeslot = relationship('Timeslot', back_populates='reservation')
