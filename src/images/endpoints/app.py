"""
This module defines the FastAPI application for the images endpoints.

The `images` router is included in the application to handle the endpoints related to
images.
"""

from fastapi import FastAPI

from src.images.endpoints.config import setup_logger
from src.images.endpoints.image import router as image_router
from ..settings.base import Settings


settings = Settings()


app = FastAPI(
    title=settings.app_name,
    description=settings.description,
    debug=settings.debug,
)
app.include_router(image_router)

setup_logger()
