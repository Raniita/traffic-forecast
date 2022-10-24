from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

import logging

from src.database.register import register_tortoise
from src.database.config import TORTOISE_ORM
from src.config import settings

logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    # enable schemas
    Tortoise.init_models(["src.database.models"], "models")
    
    app = FastAPI(
        openapi_tags=settings.TAG_METADATA,
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        version=settings.VERSION
    )

    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # Enable logging
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.info("Starting up...")

    # Setting up database & models
    register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)

    # Setting up routes
    from src.routes import networks, interfaces

    app.include_router(networks.router)
    app.include_router(interfaces.router)

    # Default endpoint
    @app.get("/", include_in_schema=False)
    async def home():
        return f"Welcome to {settings.TITLE} API! Go to '/docs' or '/redoc' to view the API definition."

    return app

app = create_app()