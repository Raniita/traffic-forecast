import pandas as pd
import random
from fastapi import HTTPException, File
from tortoise.exceptions import DoesNotExist

from src.main import logger
from src.database.models import Networks, Interfaces
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

    interfaces = df["interface"].unique()
    logger.info(f"Interfaces found on dataframe: {interfaces}")

    fields = ["RX", "TX"]
    for inter in interfaces:
        logger.info(f"Processing interface: {inter}")
        df_if = df[df.interface == inter]

        # Create interface
        inter_dict = dict()
        inter_dict = {"id_interface": str(random.randint(0, 1000)),
                      "name": inter,
                      "description": "imported interface",
                      "network_id": db_net.id}
        influx_rx = (str(inter_dict.get("name")) + '-' + str(inter_dict.get("id_interface")) + '-RX').strip()
        influx_tx = (str(inter_dict.get("name")) + '-' + str(inter_dict.get("id_interface")) + '-TX').strip()
        await Interfaces.create(**inter_dict, influx_rx=influx_rx,
                                              influx_tx=influx_tx)
        logger.info("Interface created")

    # Filter CSV with each field on pandas

    # Push points to influxDB

    # Return Status if success or error
    
    return "Adding test data.."
