from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, Movie, Favorite
from app.favorite.schemas import FavoriteMovieResponse


class FavoriteService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_favorite(self, user_id: int, movie_id: int):
        user = await self.db.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        movie = await self.db.get(Movie, movie_id)
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")

        existing_favorite = await self.db.execute(
            select(Favorite).where(
                Favorite.user_id == user_id, Favorite.movie_id == movie_id
            )
        )

        if existing_favorite.scalars().first():
            await self.db.rollback()
            raise HTTPException(status_code=404, detail="Movie already in favorites")

        fav = Favorite(user_id=user_id, movie_id=movie_id)
        self.db.add(fav)
        await self.db.commit()
        return fav

    async def delete_favorite(self, user_id: int, movie_id: int):
        query = await self.db.execute(
            select(Favorite).where(
                Favorite.user_id == user_id, Favorite.movie_id == movie_id
            )
        )
        favorite_instance = query.scalars().first()

        if not favorite_instance:
            raise HTTPException(status_code=404, detail="Favorite movie not found")

        await self.db.delete(favorite_instance)
        await self.db.commit()
        return True

    async def get_favorites(self, user_id: int):
        favorites = await self.db.execute(
            select(Movie).join(Favorite).where(Favorite.user_id == user_id)
        )
        fav_movies = favorites.scalars().all()
        return [FavoriteMovieResponse.model_validate(movie) for movie in fav_movies]
