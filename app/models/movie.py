from sqlalchemy import Integer, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[int] = mapped_column(String)
    release_year: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint(
            "release_year >= 1 AND release_year <= 9999", name="check_release_year"
        ),
    )
    country: Mapped[str] = mapped_column(String(length=60))
    director: Mapped[str] = mapped_column(String(100))

    favorites = relationship(
        "Favorite", back_populates="movie", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"{self.id} | {self.title}"
