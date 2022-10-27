from pydantic import BaseModel


class Point(BaseModel):
    timestamp: str
    link_count: str