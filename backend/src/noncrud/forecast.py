import pandas as pd
from prophet import Prophet
from fastapi import HTTPException
from fastapi.responses import PlainTextResponse
from tortoise.exceptions import DoesNotExist

from src.main import logger
from src.config import settings
from src.database.models import Networks, Interfaces
from src.schemas.networks import NetworkDatabaseSchema
from src.schemas.interfaces import InterfaceDatabaseSchema
from src.utils.influxdb import query_5m as influx_query_5m

async def forecast_interface(network_id: str, interface_id: str, field: str, periods: str, to_csv):
    # Verify that networks exists
    try:
        db_net = await NetworkDatabaseSchema.from_queryset_single(Networks.get(id_network=network_id))
    
        influx_network = db_net.influx_net
    except DoesNotExist:
        raise HTTPException(status_code=401, detail=f"Network ID {network_id} not found.")

    # Verify that interface exists on network
    try:
        db_if = await InterfaceDatabaseSchema.from_queryset_single(Interfaces.get(network=db_net.id, id_interface=interface_id))
    
        if field.upper() == "RX":
            influx_interface = db_if.influx_rx
        elif field.upper() == "TX":
            influx_interface = db_if.influx_tx
        else:
            logger.info("Field not valid")
            raise DoesNotExist
    except DoesNotExist:
        raise HTTPException(status_code=401, detail=f"Interface ID {interface_id} doesnt exists.")
    
    logger.info("Network ID and Interface ID verified")

    # Verify periods
    time_periods = int(periods)
    if time_periods < 0:
        raise HTTPException(status_code=404, detail=f"Periods must be greater than 0.")
    elif time_periods >= 365:
        time_periods = 365      # Max time fixed to one year

    # Query samples on influxdb
    result_df = influx_query_5m(influx_network=influx_network,
                                influx_interface=influx_interface)
    logger.info(f"Result query: {result_df}")
    logger.info(f"Type query result: {type(result_df)}")

    # Prophet things here!
    df_prophet = result_df[["time", "value"]]
    df_prophet.columns = ['ds', 'y']            # Must be fixed, prophet things
    
    try:
        df_prophet['ds'] = pd.to_datetime(df_prophet['ds'])
        df_prophet['ds'] = df_prophet['ds'].dt.tz_convert(None)
    except TypeError:
        logger.info("[Forecast] Skipping timezone")
        df_prophet['ds'] = df_prophet['ds']

    logger.info(df_prophet.head())

    logger.info(f"[Forecast] Creating Prophet")

    model = Prophet(seasonality_mode='multiplicative')
    logger.info(f"[Forecast] Fitting the model")
    model.fit(df_prophet)

    # Forecasting future 
    logger.info("[Forecast] Predict the future")
    future = model.make_future_dataframe(periods=time_periods)
    df_forecast = model.predict(future)

    logger.info(f"[Forecast]: \n {df_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper', 'trend', 'trend_lower', 'trend_upper']].tail()}")

    return_df = df_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper', 'trend', 'trend_lower', 'trend_upper']]
    
    # Return data to client
    if to_csv:
        return PlainTextResponse(return_df.to_csv(index=False), media_type="text/csv")
    else:
        return PlainTextResponse(return_df.to_json(orient="index", date_format="iso"), media_type="application/json")
