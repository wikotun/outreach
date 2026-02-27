"""Outreach application main entry point.

This module configures and starts the FastAPI application,
including database initialization, router registration,
and exception handlers.
"""

import json
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from config.db import init_db
from config.app_config import settings
from routes.event_type_routes import router as event_type_router
from routes.event_routes import router as event_router
from routes.participant_routes import router as participant_router
from routes.user_routes import router as user_router
from routes.security_routes import router as security_router
from alembic import command
from alembic.config import Config
import logging
import tracemalloc
from typing import AsyncGenerator

logger = logging.getLogger('main')


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application startup and shutdown lifecycle.

    Initializes the database on startup. Can optionally apply
    Alembic migrations if uncommented.

    Args:
        app: The FastAPI application instance.

    Yields:
        Control to the application after startup is complete.
    """
    init_db()
    # Apply migrations
    # alembic_cfg = Config("alembic.ini")
    # command.upgrade(alembic_cfg, "head")
    yield


app = FastAPI(lifespan=lifespan)

tracemalloc.start()



@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> PlainTextResponse:
    """Handle HTTP exceptions and return plain text responses.

    Args:
        request: The incoming request that caused the exception.
        exc: The HTTP exception that was raised.

    Returns:
        Plain text response with the error detail and status code.
    """
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> PlainTextResponse:
    """Handle request validation errors.

    Args:
        request: The incoming request that failed validation.
        exc: The validation error containing details about what failed.

    Returns:
        Plain text response with validation error details and 400 status.
    """
    return PlainTextResponse(str(exc), status_code=400)


# Include routers
app.include_router(event_type_router)
app.include_router(event_router)
app.include_router(participant_router)
app.include_router(user_router)
app.include_router(security_router)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port, log_level=settings.log_level)
