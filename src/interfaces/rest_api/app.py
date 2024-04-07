from __future__ import annotations

from fastapi import FastAPI

from src.interfaces.rest_api.v1.router import router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app
