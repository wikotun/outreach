import json
import uvicorn
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

app = FastAPI()


@app.on_event("startup")
def startup_event():
    init_db()
    # Apply migrations
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


# Include routers
app.include_router(event_type_router)
app.include_router(event_router)
app.include_router(participant_router)
app.include_router(user_router)
app.include_router(security_router)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port, log_level=settings.log_level)
