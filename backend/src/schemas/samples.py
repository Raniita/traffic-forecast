from pydantic import BaseModel


class PointSchema(BaseModel):
    timestamp: str
    link_count: str