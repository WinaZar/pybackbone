from __future__ import annotations

import uuid

from pydantic import BaseModel, ConfigDict


class ExampleEntity(BaseModel):
    id: uuid.UUID | None = None
    name: str
    description: str

    model_config = ConfigDict(from_attributes=True)
