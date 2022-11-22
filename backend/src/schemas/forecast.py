from typing import Optional, Literal
from pydantic import BaseModel, Field


class ForecastOptionsSchema(BaseModel):
    # Seasonality Mode
    #mode: str                                                  # Default: additive. Other option: multiplicative
    # Holidays Region
    holidays_region: str = Field(..., example="ES")            # Default: none, example: ES, US, ...
    # Regresion penalty
    flexibility_trend: float = Field(..., example=0.05)        # Default: 0.05, maybe tunned [0.001 0.5]
    flexibility_season: float = Field(..., example=10)         # Default: 10, maybe tunned [0.01 10]
    flexibility_holidays: float = Field(..., example=10)       # Default: 10, maybe tunned [0.01 10]


class ForecastSchema(BaseModel):
    id_network: int = Field(..., example=0)
    id_interface: int = Field(..., example=0)
    field: Literal['RX', 'TX']
    days: int = Field(..., example=365)
    options: Optional[ForecastOptionsSchema]
