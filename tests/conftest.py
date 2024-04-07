from __future__ import annotations

import typing

import pytest

from sqlalchemy_utils.functions.database import (
    create_database,
    database_exists,
    drop_database,
)

from src.common.settings.core import service_settings
from src.infrastructure.postgresql.database import DatabaseSessionManager
from src.infrastructure.postgresql.models import Base

if typing.TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from src.common.settings.core import Settings


pytest_plugins = ["tests.entities_factories"]


@pytest.fixture(scope="session")
def settings() -> Settings:
    service_settings.postgres_db = "test_database"
    return service_settings


@pytest.fixture(scope="session")
def db_session_manager(settings: Settings) -> DatabaseSessionManager:
    return DatabaseSessionManager(settings=settings)


@pytest.fixture(scope="session", autouse=True)
def _create_database(db_session_manager: DatabaseSessionManager) -> None:
    if database_exists(db_session_manager._sqlalchemy_url):
        drop_database(db_session_manager._sqlalchemy_url)
    create_database(db_session_manager._sqlalchemy_url)


@pytest.fixture(scope="function")
async def db_session(db_session_manager: DatabaseSessionManager) -> typing.AsyncGenerator[AsyncSession, None]:
    async with db_session_manager.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with db_session_manager.session() as session:
        yield session
    async with db_session_manager.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
