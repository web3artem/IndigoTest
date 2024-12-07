from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from .schemas import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def check_existing_user(self, *args):
        """Проверка на наличие пользователя в базе"""
        existing_user = await self.db.execute(
            select(User).where(User.nickname == args[0].nickname)
        )
        if existing_user.scalars().first():
            raise HTTPException(status_code=404, detail="User already exists")

    async def user_create(self, user: UserCreate):
        """Создание пользователя"""
        await self.check_existing_user(user)

        new_user = User(**user.model_dump())
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        return new_user

    async def user_delete(self, user_id: int):
        """Удаление пользователя"""
        res = await self.db.execute(select(User).where(User.id == user_id))
        user = res.scalars().first()
        if user is None:
            return None
        await self.db.delete(user)
        await self.db.commit()
        return True

    async def user_update(self, user_id: int, updated_user: UserUpdate):
        """Изменение пользователя"""
        await self.check_existing_user(updated_user)
        res = await self.db.execute(select(User).where(User.id == user_id))
        user = res.scalars().first()

        if not user:
            return None

        for field, value in updated_user.model_dump(exclude_unset=True).items():
            setattr(user, field, value)

        await self.db.commit()

        return user
