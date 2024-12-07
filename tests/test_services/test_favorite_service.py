import pytest

from app.favorite.services import FavoriteService
from app.user.services import UserService
from app.user.schemas import UserCreate
from app.movie.services import MovieService
from movie.schemas import MovieCreate


@pytest.mark.asyncio
async def test_add_favorite(async_session):
    async for session in async_session:
        favorite_service = FavoriteService(session)
        user_service = UserService(session)
        movie_service = MovieService(session)

        user_data = UserCreate(first_name="Test", second_name="Test2", nickname="Test3")
        movie_data = MovieCreate(
            title="Catch Me If You Can",
            release_year=2002,
            country="United states",
            director="Steven Spielberg",
        )

        user = await user_service.user_create(user_data)
        movie = await movie_service.movie_create(movie_data)

        fav = await favorite_service.add_favorite(user.id, movie.id)

        assert fav.user_id == user.id
        assert fav.movie_id == movie.id


@pytest.mark.asyncio
async def test_delete_favorite(async_session):
    async for session in async_session:
        favorite_service = FavoriteService(session)
        user_service = UserService(session)
        movie_service = MovieService(session)
        user_data = UserCreate(first_name="Test", second_name="Test2", nickname="Test3")
        movie_data = MovieCreate(
            title="Catch Me If You Can",
            release_year=2002,
            country="United states",
            director="Steven Spielberg",
        )

        user = await user_service.user_create(user_data)
        movie = await movie_service.movie_create(movie_data)

        await favorite_service.add_favorite(user.id, movie.id)
        fav = await favorite_service.delete_favorite(user.id, movie.id)

        assert fav is True


@pytest.mark.asyncio
async def test_get_favorites(async_session):
    async for session in async_session:
        favorite_service = FavoriteService(session)
        user_service = UserService(session)
        movie_service = MovieService(session)
        user_data = UserCreate(first_name="Test", second_name="Test2", nickname="Test3")
        movie_data = MovieCreate(
            title="Catch Me If You Can",
            release_year=2002,
            country="United states",
            director="Steven Spielberg",
        )

        user = await user_service.user_create(user_data)
        movie = await movie_service.movie_create(movie_data)
        await favorite_service.add_favorite(user.id, movie.id)

        fav_list = await favorite_service.get_favorites(user.id)
        assert fav_list[0].title == "Catch Me If You Can"
        assert fav_list[0].release_year == 2002
