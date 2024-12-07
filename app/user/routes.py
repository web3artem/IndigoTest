from fastapi import APIRouter, Depends, HTTPException
from fastapi.exceptions import ResponseValidationError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import db
from .services import UserService
from .schemas import UserCreate, UserUpdate

router = APIRouter(tags=["user"])


@router.post("/create", status_code=201, response_model=UserCreate)
async def create_user(
    data: UserCreate, session: AsyncSession = Depends(db.get_async_session)
):
    """Создание юзера"""
    try:
        new_user = await UserService(session).user_create(data)
        return new_user
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())


@router.put("/change/{user_id}", response_model=UserUpdate)
async def change_user_data(
    user_id: int,
    data: UserUpdate,
    session: AsyncSession = Depends(db.get_async_session),
):
    """Изменение юзера"""
    try:
        updated_user = await UserService(session).user_update(user_id, data)
        if updated_user is None:
            raise HTTPException(status_code=404, detail="User  not found")
        return updated_user
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())


@router.delete("/delete/{user_id}", status_code=204)
async def delete_user(
    user_id: int, session: AsyncSession = Depends(db.get_async_session)
):
    result = await UserService(session).user_delete(user_id)

    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return None
