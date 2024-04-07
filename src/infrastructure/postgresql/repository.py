from __future__ import annotations

import typing
import uuid

from sqlalchemy import select, insert, update

from src.common.entities.core import ExampleEntity
from src.infrastructure.postgresql.models import ExampleEntityModel

if typing.TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class PostgresqlRepository:
    @staticmethod
    async def create_example_entity(
        session: AsyncSession, entity: ExampleEntity, commit: bool = False
    ) -> ExampleEntity:
        result = await session.execute(insert(ExampleEntityModel).returning(ExampleEntityModel), [entity.model_dump()])
        if commit:
            await session.commit()
        else:
            await session.flush()
        return ExampleEntity.model_validate(result.scalar_one())

    @staticmethod
    async def update_example_entity(session: AsyncSession, entity: ExampleEntity, commit: bool = False) -> None:
        if entity.id is None:
            raise ValueError("Entity id is required")
        await session.execute(update(ExampleEntityModel).returning(ExampleEntityModel), [entity.model_dump()])
        if commit:
            await session.commit()
        else:
            await session.flush()

    @staticmethod
    async def get_example_entity_or_none(session: AsyncSession, entity_id: uuid.UUID) -> ExampleEntity:
        result = await session.execute(select(ExampleEntityModel).where(ExampleEntityModel.id == entity_id))
        return ExampleEntity.model_validate(result.scalar_one_or_none())
