from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from tortoise import Tortoise

# Disable pivot warning for influxdb
from influxdb_client.client.warnings import MissingPivotFunction
import warnings

import logging

from src.database.register import register_tortoise
from src.database.config import TORTOISE_ORM
from src.config import settings

logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    # enable schemas
    Tortoise.init_models(["src.database.models"], "models")
    
    app = FastAPI(
        debug=settings.DEBUG,
        openapi_tags=settings.TAG_METADATA,
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        swagger_ui_parameters={"defaultModelsExpandDepth": 0}       # -1: disable, 0: collapsed, 1: enable
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
    #formatter = logging.Formatter("%(asctime)s - %(module)s - %(funcName)s - %(levelname)s - %(message)s")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.info("Starting up...")

    # Setting up database & models
    register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)

    # Verify influxdb connection
    from src.utils.influxdb import check_influxdb, check_query, check_write
    logger.info(f"[InfluxDB] >> URL: {settings.INFLUX_URL}, Bucket: {settings.INFLUX_BUCKET}, Org: {settings.INFLUX_ORG}")
    check_influxdb()
    check_query()
    check_write()

    # Disable Pivot warning InfluxDB
    warnings.simplefilter("ignore", MissingPivotFunction)

    # Setting up routes
    from src.routes import networks, interfaces, samples, query, forecasts

    app.include_router(networks.router)
    app.include_router(interfaces.router)
    app.include_router(samples.router)
    app.include_router(query.router)
    app.include_router(forecasts.router)

    # Enable FastAPI-Pagination
    add_pagination(app)

    # Default endpoint
    @app.get("/", include_in_schema=False)
    async def home():
        return f"Welcome to {settings.TITLE} API! Go to '/docs' or '/redoc' to view the API definition."

    return app

app = create_app()