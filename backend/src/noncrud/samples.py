import pandas as pd
from fastapi import HTTPException, File
from tortoise.exceptions import DoesNotExist

from src.main import logger
from src.database.models import Networks
from src.schemas.networks import NetworkDatabaseSchema
from src.utils.influxdb import check_exists_network as influxdb_exists_network

async def add_test_data(network_id: str, file):
    # Verify that networks exists
    try:
        db_net = await NetworkDatabaseSchema.from_queryset_single(Networks.get(id_network=network_id))
    except DoesNotExist:
        raise HTTPException(status_code=401, detail=f"Network ID not found.")

    # Verify that network on influx exists
    if influxdb_exists_network(influx_network=db_net.influx_net):
        logger.info("Network exists")
    else:
        raise HTTPException(status_code=401, detail=f"Network not found on database.")

    # Read CSV with pandas
    df = pd.read_csv(file)
    logger.info(f"Dataframe upload: {df}")

    # Filter CSV with each field on pandas

    # Push points to influxDB

    # Return Status if success or error
    
    return "Adding test data.."
