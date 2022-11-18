from pydantic import BaseModel

class ForecastSchema(BaseModel):
    network_id: str
    interface_id: str
    field: str
    periods: str