from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Favorite(Base):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    movie_id: Mapped[int] = mapped_column(Integer, ForeignKey("movies.id"))

    user = relationship("User", back_populates="favorites")
    movie = relationship("Movie", back_populates="favorites")
