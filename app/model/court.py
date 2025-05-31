from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.utils.database import Base

class Court(Base):
    __tablename__ = 'court'
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(unique=True)
    location : Mapped[str] = mapped_column(nullable=False)

    timeslots = relationship("Timeslot", backref="court")
    reservation = relationship("Reservation", backref="court")