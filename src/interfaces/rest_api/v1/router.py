from __future__ import annotations

from fastapi import APIRouter

from src.common.entities.core import ExampleEntity
from src.interfaces.rest_api.dependencies import DatabaseSession
from src.application.services.core import create_example_entity

router = APIRouter(prefix="/v1")


@router.post("/create_entity")
async def create_entity(entity: ExampleEntity, session: DatabaseSession) -> ExampleEntity:
    created_entity = await create_example_entity(entity=entity, session=session)
    return created_entity
