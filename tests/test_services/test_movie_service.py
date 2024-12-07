import pytest
from pydantic import ValidationError

from movie.services import MovieService
from movie.schemas import MovieCreate, MovieUpdate


@pytest.mark.asyncio
async def test_movie_create(async_session):
    async for session in async_session:
        movie_service = MovieService(session)
        movie_data = MovieCreate(
            title="Catch Me If You Can",
            release_year=2002,
            country="United states",
            director="Steven Spielberg",
        )
        movie = await movie_service.movie_create(movie_data)

        assert movie.title == "Catch Me If You Can"
        assert movie.country == "United states"
        assert movie.director == "Steven Spielberg"


@pytest.mark.parametrize("release_year", [0, 10000, -1, "invalid"])
def test_movie_create_validation(release_year):
    """Проверка на некорректный release_year"""
    with pytest.raises(ValidationError):
        MovieCreate(
            title="Catch Me If You Can",
            release_year=release_year,
            country="United states",
            director="Steven Spielberg",
        )


@pytest.mark.asyncio
async def test_movie_update(async_session):
    async for session in async_session:
        movie_service = MovieService(session)
        movie_data = MovieCreate(
            title="Catch Me If You Can",
            release_year=2002,
            country="United states",
            director="Steven Spielberg",
        )
        movie = MovieUpdate(
            title="Se7en18",
            release_year=1995,
            country="United states",
            director="David Fincher",
        )
        await movie_service.movie_create(movie_data)
        movie_updated = await movie_service.movie_update(1, movie)

        assert movie_updated.title == "Se7en18"
        assert movie_updated.release_year == 1995
        assert movie_updated.country == "United states"
        assert movie_updated.director == "David Fincher"


@pytest.mark.asyncio
async def test_movie_delete(async_session):
    async for session in async_session:
        movie_service = MovieService(session)
        movie_data = MovieCreate(
            title="Catch Me If You Can",
            release_year=2002,
            country="United states",
            director="Steven Spielberg",
        )
        await movie_service.movie_create(movie_data)

        assert await movie_service.movie_delete(movie_id=1) is True
        assert await movie_service.movie_delete(movie_id=100) is None
