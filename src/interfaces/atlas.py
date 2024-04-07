from __future__ import annotations

import typing

from sqlalchemy import create_mock_engine

from src.infrastructure.postgresql.models import Base

if typing.TYPE_CHECKING:
    from sqlalchemy.orm import DeclarativeBase


def dump_ddl(dialect_driver: str, base: typing.Type[DeclarativeBase]) -> typing.Type[DeclarativeBase]:
    """
    Creates a mock engine and dumps its DDL to stdout
    """

    def dump(sql, *multiparams, **params) -> None:  # type: ignore
        print(str(sql.compile(dialect=engine.dialect)).replace("\t", "").replace("\n", ""), end=";\n\n")

    engine = create_mock_engine(f"{dialect_driver}://", dump)
    base.metadata.create_all(engine, checkfirst=False)
    return base


def atlas_generate_migrations() -> None:
    dump_ddl("postgresql", Base)
