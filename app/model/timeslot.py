from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey
from app.utils.database import Base
from datetime import date, time

class TimeSlot(Base):
    __tablename__ = 'time_slot'
    id : Mapped[int] = mapped_column(primary_key=True)
    start_time : Mapped[time] = mapped_column(nullable=False)
    end_time : Mapped[time] = mapped_column(nullable=False)
    date : Mapped[date] = mapped_column(nullable=False)
    court_id : Mapped[int] = mapped_column(ForeignKey('court.id'))
    reservation_id : Mapped[int] = mapped_column(ForeignKey('reservation.id'))

    court = relationship('Court', back_populates='time_slots')
    reservation = relationship('Reservation', back_populates='time_slots')