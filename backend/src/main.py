from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

import logging

from src.database.register import register_tortoise
from src.database.config import TORTOISE_ORM

logger = logging.getLogger(__name__)

def create_app()->FastAPI:
    # enable schemas
    Tortoise.init_models(["src.database.models"], "models")
    
    app = FastAPI()

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

    @app.get("/")
    async def home():
        return "Hello, World!"

    return app

app = create_app()