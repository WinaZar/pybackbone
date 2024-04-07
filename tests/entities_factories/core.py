from __future__ import annotations

from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.pytest_plugin import register_fixture

from src.common.entities.core import ExampleEntity


@register_fixture
class ExampleEntityFactory(ModelFactory[ExampleEntity]): ...
