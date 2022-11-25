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
        Execute a forecast given a the next data:

        * **id_network**: Number for identificate a network
        * **id_interface**: Number for identificate an interface
        * **field**: Select over **RX** or **TX**
        * **days**: Number of days to forecast
        * **options**:
            - **holidays_region**: Set region holidays (_default: "ES"_)
            - **flexibility_trend**: Suggested tunning over [0.001 0.5] (_default: 0.05_)
            - **flexibility_season**: Suggested tunning over [0.01 10] (_default: 10_)
            - **flexibility_holidays**: Suggested tunning over [0.01 10] (_default: 10_)

        Parameters:
        * **to_csv**: Enable output on CSV, default output is a JSON.



    """

    return await forecasts.forecast_interface(network_id=forecast_in.id_network, 
                                 interface_id=forecast_in.id_interface,
                                 field=forecast_in.field,
                                 periods=forecast_in.days,
                                 options=forecast_in.options,
                                 to_csv=to_csv)