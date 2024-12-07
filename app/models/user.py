from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(length=50))
    second_name: Mapped[str] = mapped_column(String(length=50))
    nickname: Mapped[str] = mapped_column(String(length=50), unique=True)

    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"{self.id} | {self.nickname}"
