from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from enum import Enum
from app.model.abstract import AbstractBaseModel


class RoleEnum(Enum):
    user = 'user'
    admin = 'admin'


class User(AbstractBaseModel):
    __tablename__ = 'user'
    username : Mapped[str] = mapped_column(unique=True)
    email : Mapped[str] = mapped_column(unique=True)
    password : Mapped[str] = mapped_column(nullable=False)
    role : Mapped[str] = mapped_column(SQLAlchemyEnum(RoleEnum),default=RoleEnum.user)

    reservations = relationship("Reservation",back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    access_tokens = relationship("AccessToken", back_populates="user", cascade="all, delete-orphan")
    def __str__(self) -> str:
        return self.username

