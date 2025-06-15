import json
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse, PlainTextResponse
from config.db import init_db
from config.app_config import settings
from routes.event_type_routes import router as event_type_router
from routes.event_routes import router as event_router
from routes.participant_routes import router as participant_router
from routes.user_routes import router as user_router
from routes.security_routes import router as security_router
from alembic import command
from alembic.config import Config


load_dotenv()
app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()
    # Apply migrations
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


# @app.exception_handler(HTTPException)
# async def http_exception_handler(request, exc):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={
#             "detail": exc.detail
#         },
#     )
#
#
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return PlainTextResponse(
#         "This is a plain text response:"
#         f"\n{json.dumps(exc.errors(), indent=2)}",
#         status_code=status.HTTP_400_BAD_REQUEST,
#     )

    # Include routers
    app.include_router(event_type_router)
    app.include_router(event_router)
    app.include_router(participant_router)
    app.include_router(user_router)
    app.include_router(security_router)
