from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from enum import Enum
from app.utils.database import Base


class RoleEnum(Enum):
    user = 'user'
    admin = 'admin'


class User(Base):
    __tablename__ = 'user'
    id : Mapped[int] = mapped_column(primary_key=True)
    username : Mapped[str] = mapped_column(unique=True)
    email : Mapped[str] = mapped_column(unique=True)
    password : Mapped[str] = mapped_column(nullable=False)
    role : Mapped[str] = mapped_column(SQLAlchemyEnum(RoleEnum),default=RoleEnum.user)

    reservation = relationship("Reservation",back_populates="user")