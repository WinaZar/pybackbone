from __future__ import annotations

import typer
import uvicorn

from src.interfaces.atlas import atlas_generate_migrations
from src.common.settings.core import service_settings


cli = typer.Typer()


@cli.command()
def ping() -> None:
    typer.echo("pong")


@cli.command()
def generate_migrations() -> None:
    """Command to dump models ddl for the Atlas migration tool."""

    atlas_generate_migrations()


@cli.command()
def run_web() -> None:
    """Command to run the FastAPI web server."""

    uvicorn.run(
        "src.interfaces.rest_api.app:create_app",
        factory=True,
        port=service_settings.uvicorn_port,
        log_level=service_settings.uvicorn_log_level,
        reload=service_settings.debug,
    )


cli()
