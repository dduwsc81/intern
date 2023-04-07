from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.api_v1.api import api_router
from app.core.config import settings
import firebase_admin
from .middleware import AdminMiddleware
from requests import Request
from fastapi.responses import JSONResponse
from app.middleware_log.route_logger import RouteLoggerMiddleware
import os
import json

import logging
import logging.config
import os
from os import path

# Config logging
log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.conf")
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Init middleware
app.add_middleware(RouteLoggerMiddleware)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers='Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


# middleware
# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     middleware = AdminMiddleware().check_role(request)
#     if middleware:
#         response = await call_next(request)
#         return response
#     else:
#         return JSONResponse(status_code=401, content={"detail": "Unauthorized by user's role"})
#

firebase_admin.initialize_app()
