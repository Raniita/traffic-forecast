import os, pathlib
from functools import lru_cache

class BaseConfig:
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent

    SECRET_KEY: str = os.environ.get('SECRET_KEY', 'traffic-forecast')

    # Database config {Postgres13}
    POSTGRES_USER: str = os.environ.get('POSTGRES_USER', 'admin')
    POSTGRES_PASSWORD: str = os.environ.get('POSTGRES_PASSWORD', 'none')
    POSTGRES_DB: str = os.environ.get('POSTGRES_DB', 'traffic-forecast')

    DATABASE_URL: str = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}"

    # Boolean to enable logging to file
    FILE_LOG: str = os.environ.get('FILE_LOG', 'false')

class DevelopmentConfig(BaseConfig):
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
