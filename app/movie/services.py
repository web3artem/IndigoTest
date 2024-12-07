from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Movie
from app.movie.schemas import MovieCreate, MovieUpdate


class MovieService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def movie_create(self, movie: MovieCreate):
        """Добавление нового фильма"""
        new_movie = Movie(**movie.model_dump())
        self.db.add(new_movie)
        await self.db.commit()
        await self.db.refresh(new_movie)
        return new_movie

    async def movie_delete(self, movie_id: int):
        res = await self.db.execute(select(Movie).where(Movie.id == movie_id))
        movie = res.scalars().first()
        if movie is None:
            return None
        await self.db.delete(movie)
        await self.db.commit()
        return True

    async def movie_update(self, movie_id: int, updated_movie: MovieUpdate):
        res = await self.db.execute(select(Movie).where(Movie.id == movie_id))
        film = res.scalars().first()

        if not film:
            return None

        for field, value in updated_movie.model_dump(exclude_unset=True).items():
            setattr(film, field, value)

        await self.db.commit()

        return film
