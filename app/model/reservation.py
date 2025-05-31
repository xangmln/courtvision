from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from app.utils.database import Base
from datetime import date

class Reservation(Base):
    __tablename__ = 'reservation'
    id : Mapped[int] = mapped_column(primary_key=True)
    user_id : Mapped[int] = mapped_column(ForeignKey('user.id'))
    court_id : Mapped[int] = mapped_column(ForeignKey('court.id'))
    timeslot_id : Mapped[int] = mapped_column(ForeignKey('timeslot.id'))
    member : Mapped[int] = mapped_column(default=1)

    user = relationship('User', back_populates='reservation')
    court = relationship('Court', back_populates='reservation')
    timeslot = relationship('Timeslot', back_populates='reservation')
