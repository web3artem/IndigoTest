import pytest
from app.user.schemas import UserCreate, UserUpdate
from user.services import UserService


@pytest.mark.asyncio
async def test_user_create(async_session):
    async for session in async_session:
        user_service = UserService(session)
        user_data = UserCreate(first_name="Test", second_name="Test2", nickname="Test3")
        new_user = await user_service.user_create(user_data)
        assert new_user.first_name == "Test"
        assert new_user.second_name == "Test2"
        assert new_user.nickname == "Test3"


@pytest.mark.asyncio
async def test_user_update(async_session):
    async for session in async_session:
        user_service = UserService(session)
        user_data = UserCreate(first_name="Test", second_name="Test2", nickname="Test3")

        user = UserUpdate(
            first_name="Robby", second_name="Roblox", nickname="robby_roblox"
        )
        await user_service.user_create(user_data)
        updated_user = await user_service.user_update(1, user)

        assert updated_user.first_name == "Robby"
        assert updated_user.second_name == "Roblox"
        assert updated_user.nickname == "robby_roblox"


@pytest.mark.asyncio
async def test_user_delete(async_session):
    async for session in async_session:
        user_service = UserService(session)
        user_data = UserCreate(first_name="Test", second_name="Test2", nickname="Test3")
        await user_service.user_create(user_data)

        assert await user_service.user_delete(user_id=1) is True
        assert await user_service.user_delete(user_id=100) is None
