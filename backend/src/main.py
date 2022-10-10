from fastapi import FastAPI
import logging

logger = logging.getLogger(__name__)

def create_app()->FastAPI:
    app = FastAPI()

    # Enable logging
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.info("Starting up...")

    @app.get("/")
    async def home():
        return "Hello, World!"

    return app

app = create_app()