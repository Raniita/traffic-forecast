from typing import Union
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

import src.noncrud.forecast as forecasts
from src.schemas.forecast import ForecastSchema

router = APIRouter(prefix="/forecast",
                   tags=["Forecast"])


@router.post("/",  response_class=PlainTextResponse)
async def forecast_link_count_interface(forecast_in: ForecastSchema,
                                        to_csv: Union[bool, None] = False) -> PlainTextResponse:
    """
        Enqueue a forecast given a network_id and a interface

    """

    return await forecasts.forecast_interface(network_id=forecast_in.id_network, 
                                 interface_id=forecast_in.id_interface,
                                 field=forecast_in.field,
                                 periods=forecast_in.days,
                                 options=forecast_in.options,
                                 to_csv=to_csv)