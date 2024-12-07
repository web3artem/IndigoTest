from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


class Database:
    def __init__(self):
        self.async_engine = create_async_engine(settings.ASYNC_DATABASE_URL)
        self.async_sessionmaker = async_sessionmaker(
            self.async_engine, class_=AsyncSession, expire_on_commit=False
        )

    async def get_async_session(self) -> Generator[AsyncSession, None, None]:
        async with self.async_sessionmaker() as session:
            yield session


class Base(DeclarativeBase):
    pass


db = Database()
