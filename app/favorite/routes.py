from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.favorite.services import FavoriteService
from app.database import db

router = APIRouter(tags=["favorites"])


@router.post(
    "/users/{user_id}/favorites",
    status_code=201,
    summary="Добавление фильма в израбнное по user_id и movie_id",
)
async def add_favorite(
    user_id: int, movie_id: int, session: AsyncSession = Depends(db.get_async_session)
):
    """Добавление любимого фильма"""
    fav = await FavoriteService(session).add_favorite(user_id, movie_id)
    return fav


@router.delete(
    "/users/{user_id}/favorites/{movie_id}",
    status_code=204,
    summary="Удаление фильма из избранного по user_id и movie_id",
)
async def delete_favorite(
    user_id: int, movie_id: int, session: AsyncSession = Depends(db.get_async_session)
):
    """Удаление любимого фильма"""
    await FavoriteService(session).delete_favorite(user_id, movie_id)


@router.get("/users/{user_id}/favorites", summary="Получение всех фильмов по id юзера")
async def get_favorites(
    user_id: int, session: AsyncSession = Depends(db.get_async_session)
):
    """Получение всех любимых фильмов"""
    favorites = await FavoriteService(session).get_favorites(user_id)
    return {"message": favorites}
