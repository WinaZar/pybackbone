from __future__ import annotations

import typing

from src.common.entities.core import ExampleEntity
from src.infrastructure.postgresql.repository import PostgresqlRepository

if typing.TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def create_example_entity(*, entity: ExampleEntity, session: AsyncSession) -> ExampleEntity:
    created_entity = await PostgresqlRepository.create_example_entity(session=session, entity=entity, commit=True)
    return created_entity
