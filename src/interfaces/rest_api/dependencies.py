from __future__ import annotations

import typing

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.postgresql.database import get_database_session


DatabaseSession = typing.Annotated[AsyncSession, Depends(get_database_session)]
