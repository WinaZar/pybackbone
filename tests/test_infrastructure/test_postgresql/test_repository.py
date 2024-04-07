from __future__ import annotations

import typing

from sqlalchemy import select

from src.infrastructure.postgresql.repository import PostgresqlRepository
from src.infrastructure.postgresql.models import ExampleEntityModel


if typing.TYPE_CHECKING:
    from faker import Faker
    from sqlalchemy.ext.asyncio import AsyncSession

    from tests.entities_factories.core import ExampleEntityFactory


async def test__postgresql_repository__create_example_entity__success(
    db_session: AsyncSession, example_entity_factory: ExampleEntityFactory
) -> None:
    entity = example_entity_factory.build(id=None)

    created_entity = await PostgresqlRepository.create_example_entity(session=db_session, entity=entity, commit=True)
    fetch_result = await db_session.execute(
        select(ExampleEntityModel).where(ExampleEntityModel.id == created_entity.id)
    )
    entity_model = fetch_result.scalar_one()

    assert entity_model.id == created_entity.id
    assert entity_model.name == created_entity.name
    assert entity_model.description == created_entity.description


async def test__postgresql_repository__update_example_entity__success(
    db_session: AsyncSession, example_entity_factory: ExampleEntityFactory, faker: Faker
) -> None:
    entity = example_entity_factory.build(id=None)
    created_entity = await PostgresqlRepository.create_example_entity(session=db_session, entity=entity, commit=True)
    new_name = faker.word()
    new_description = faker.sentence()
    created_entity.name = new_name
    created_entity.description = new_description

    await PostgresqlRepository.update_example_entity(session=db_session, entity=created_entity, commit=True)
    fetch_result = await db_session.execute(
        select(ExampleEntityModel).where(ExampleEntityModel.id == created_entity.id)
    )
    entity_model = fetch_result.scalar_one()

    assert entity_model.id == created_entity.id
    assert entity_model.name == new_name
    assert entity_model.description == new_description


async def test__postgresql_repository__get_example_entity_or_none__success(
    db_session: AsyncSession, example_entity_factory: ExampleEntityFactory
) -> None:
    entity = example_entity_factory.build(id=None)
    created_entity = await PostgresqlRepository.create_example_entity(session=db_session, entity=entity, commit=True)

    fetched_entity = await PostgresqlRepository.get_example_entity_or_none(
        session=db_session,
        entity_id=created_entity.id,  # type: ignore[arg-type]
    )

    assert fetched_entity == created_entity
