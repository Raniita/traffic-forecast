import os, pathlib
from functools import lru_cache

class BaseConfig:
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent

    DEBUG: bool = False
    SECRET_KEY: str = os.environ.get('SECRET_KEY', 'traffic-forecast')

    # Database config {Postgres13}
    POSTGRES_USER: str = os.environ.get('POSTGRES_USER', 'admin')
    POSTGRES_PASSWORD: str = os.environ.get('POSTGRES_PASSWORD', 'none')
    POSTGRES_DB: str = os.environ.get('POSTGRES_DB', 'traffic-forecast')

    DATABASE_URL: str = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}"

    # Database config {InfluxDB}
    INFLUX_URL: str = os.environ.get('INFLUX_URL', "http://influxdb:8086")
    INFLUX_TOKEN: str | None = os.environ.get('INFLUX_TOKEN', None)
    INFLUX_ORG: str = os.environ.get('INFLUX_ORG', "e-lighthouse")
    INFLUX_BUCKET: str = os.environ.get('INFLUX_BUCKET', "traffic_forecast")

    # Boolean to enable logging to file
    FILE_LOG: str = os.environ.get('FILE_LOG', 'false')

    # OpenAPI definitions
    TITLE = "Traffic Forecast"
    VERSION = "0.2.2"
    DESCRIPTION = """ 
This is a microservice app for **monitor**, **store** samples and generate **forecast** of a **network traffic**. Features: 

* Add monited network, monitored interfaces, and samples. 
* Execute a traffic forecast with the objetive of predcit the traffic over the time. 
* Query the storaged samples and apply some filtering. 
    
"""

    TAG_METADATA = [
        {
            "name": "Networks",
            "description": "Operations with networks."
        },
        {
            "name": "Interfaces",
            "description": "Operations with interfaces."
        },
        {
            "name": "Samples",
            "description": "Operations with samples."
        },
        {
            "name": "Query samples",
            "description": "Operations for query monitored information."
        },
        {
            "name": "Forecast",
            "description": "Operations for execute forecast of an interface monitored traffic."
        }
    ]
    

class DevelopmentConfig(BaseConfig):
    DEBUG: bool  = True

    pass

class ProductionConfig(BaseConfig):
    pass

class TestingConfig(BaseConfig):
    pass

@lru_cache
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production" : ProductionConfig,
        "testing": TestingConfig,
    }

    config_name = os.environ.get('FASTAPI_CONFIG', 'production')
    config_cls = config_cls_dict[config_name]

    return config_cls()

settings = get_settings()
