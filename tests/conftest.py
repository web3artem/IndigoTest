from typing import Any, AsyncGenerator

import pytest
import sqlalchemy as sa
from alembic.command import upgrade, downgrade
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from app.config import Settings
from app.config import settings as app_settings
from tests.fixtures.database import get_test_alembic_config


@pytest.fixture(scope="session", autouse=True)
def settings() -> Settings:
    print("Я В СЕТТИНГС")
    return app_settings


@pytest.fixture(scope="function", autouse=True)
async def async_engine(settings) -> AsyncGenerator[AsyncEngine, Any]:
    """Создает тестовую БД и проводит миграции alembic run_migrations."""
    test_db_name = settings.test_postgres_db

    assert "test_" in test_db_name, "prod DB in tests"
    assert settings.MODE == "TEST", "you're using DEV .env"

    engine_for_create_db = create_async_engine(
        settings.ASYNC_DATABASE_URL, isolation_level="AUTOCOMMIT"
    )
    connection_for_create_test_db = await engine_for_create_db.connect()

    try:
        is_test_db_exists = await connection_for_create_test_db.execute(
            sa.text(f"SELECT 1 FROM pg_database WHERE datname = '{test_db_name}';")
        )

        if not is_test_db_exists.one_or_none():
            await connection_for_create_test_db.execute(
                sa.text(f"CREATE DATABASE {test_db_name};")
            )
        print("Тестовая БД была успешно создана")

        engine_with_test_db = create_async_engine(
            settings.test_postgres_url,
        )
        try:
            yield engine_with_test_db
        finally:
            await engine_with_test_db.dispose()

    finally:
        await connection_for_create_test_db.close()
        await engine_for_create_db.dispose()


@pytest.fixture(scope="function", autouse=True)
async def async_session(settings, async_engine):
    alembic_config = get_test_alembic_config(settings.test_postgres_url)
    async for engine in async_engine:
        async with engine.connect() as c:
            await c.run_sync(lambda _: upgrade(alembic_config, "heads"))

        get_async_session = async_sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        async with get_async_session() as session:
            yield session
            print("Session yielded; executing downgrade...")
        async with engine.connect() as c:
            await c.run_sync(lambda _: downgrade(alembic_config, "base"))
