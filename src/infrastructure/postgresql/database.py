from __future__ import annotations

import typing
import contextlib

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.common.settings.core import service_settings

if typing.TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, AsyncConnection
    from src.common.settings.core import Settings


class DatabaseSessionManager:
    def __init__(self, *, settings: Settings) -> None:
        self._settings = settings
        self._sqlalchemy_url = URL.create(
            drivername="postgresql+psycopg",
            username=settings.postgres_user,
            password=settings.postgres_password.get_secret_value(),
            host=settings.postgres_host,
            port=settings.postgres_port,
            database=settings.postgres_db,
        )
        self._engine: AsyncEngine | None = self._create_engine()
        self._sessionmaker: async_sessionmaker[AsyncSession] | None = async_sessionmaker(
            bind=self._engine, expire_on_commit=False
        )

    def _create_engine(self) -> AsyncEngine:
        engine_parameters = {
            "pool_size": 20,
            "max_overflow": 0,
        }

        if self._settings.debug:
            engine_parameters["echo"] = True
            engine_parameters["echo_pool"] = True
        engine = create_async_engine(self._sqlalchemy_url, **engine_parameters)
        return engine

    async def close(self) -> None:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> typing.AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> typing.AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(settings=service_settings)


async def get_database_session() -> typing.AsyncIterator[AsyncSession]:
    async with sessionmanager.session() as session:
        yield session
