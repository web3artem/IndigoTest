from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import db
from app.movie.services import MovieService
from app.movie.schemas import MovieUpdate, MovieCreateWithEnum, MovieUpdateWithEnum

from app.movie.utils import convert_movie_schema

router = APIRouter(tags=["movie"])


@router.post(
    "/create",
    response_model=MovieCreateWithEnum,
    status_code=201,
    summary="Добавление фильма",
    description="Поле country реализовано через Enum, посмотреть все страны можно введя некорректное значение",
)
async def create_movie(
    movie: MovieCreateWithEnum, session: AsyncSession = Depends(db.get_async_session)
):
    """Добавление фильма"""
    updated_movie = convert_movie_schema(movie)
    try:
        new_movie = await MovieService(session).movie_create(updated_movie)
        return new_movie
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Произошла ошибка сервера.")


@router.put(
    "/change/{movie_id}",
    response_model=MovieUpdate,
    summary="Изменение одного или нескольких полей в фильме",
)
async def change_movie_data(
    movie_id: int,
    data: MovieUpdateWithEnum,
    session: AsyncSession = Depends(db.get_async_session),
):
    """Изменение фильма"""
    movie_data = convert_movie_schema(data)
    try:
        updated_movie = await MovieService(session).movie_update(movie_id, movie_data)
        return updated_movie
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Произошла ошибка сервера.")


@router.delete(
    "/delete/{movie_id}", status_code=204, summary="Удаление фильма по movie_id"
)
async def delete_movie(
    movie_id: int, session: AsyncSession = Depends(db.get_async_session)
):
    """Удаление фильма"""
    result = await MovieService(session).movie_delete(movie_id)

    if not result:
        raise HTTPException(status_code=404, detail="Movie not found")
