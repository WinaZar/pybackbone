from __future__ import annotations

import typing

from src.application.services.core import create_example_entity

if typing.TYPE_CHECKING:
    from pytest_mock import MockerFixture

    from tests.entities_factories.core import ExampleEntityFactory


async def test__create_example_entity__success(
    example_entity_factory: ExampleEntityFactory, mocker: MockerFixture
) -> None:
    db_session = mocker.MagicMock()
    entity = example_entity_factory.build()
    postgresql_repository__create_example_entity__mock = mocker.patch(
        "src.application.services.core.PostgresqlRepository.create_example_entity"
    )

    created_entity = await create_example_entity(entity=entity, session=db_session)

    assert created_entity == postgresql_repository__create_example_entity__mock.return_value
    postgresql_repository__create_example_entity__mock.assert_awaited_once_with(
        session=db_session, entity=entity, commit=True
    )
