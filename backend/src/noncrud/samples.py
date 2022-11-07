import pandas as pd
import random
from fastapi import HTTPException, File
from tortoise.exceptions import DoesNotExist, IntegrityError

from src.main import logger
from src.config import settings
from src.database.models import Networks, Interfaces
from src.schemas.networks import NetworkDatabaseSchema
from src.schemas.messages import Status
from src.utils.influxdb import check_exists_network as influxdb_exists_network
from src.utils.influxdb import create_write_api as influxdb_create_write_api

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

    write_api = influxdb_create_write_api()
    fields = ["RX", "TX"]
    for inter in interfaces:
        logger.info(f"Processing interface: {inter}")
        df_if = df[df.interface == inter]

        # Create interface
        try:
            inter_dict = dict()
            inter_dict = {"id_interface": str(random.randint(0, 1000)),
                          "name": inter,
                          "description": "imported interface",
                          "network_id": db_net.id}
            influx_rx = (str(inter_dict.get("id_interface")) + '-' + str(inter_dict.get("name")) + '-RX').strip()
            influx_tx = (str(inter_dict.get("id_interface")) + '-' + str(inter_dict.get("name")) + '-TX').strip()
            interface_influx = [influx_rx, influx_tx]       # Same order as fields
            await Interfaces.create(**inter_dict, influx_rx=influx_rx,
                                                  influx_tx=influx_tx)
        except IntegrityError:
            raise HTTPException(status_code=401, detail=f"Unable to create interfaces on database.")
        logger.info("Interface created")

        # Filter CSV with each field on pandas
        for i in range(0, len(fields)):
            logger.info(f"Field: {fields[i]}")
            df_field = df_if[["timestamp", "interface", fields[i]]]

            # Adapt dataframe to InfluxDB format
            #df_field = df_field.drop(columns=["interface"])
            #df_field["_measurement"] = db_net.influx_net
            df_field["interface"] = interface_influx[i]
            df_field = df_field.rename(columns={"timestamp": "_time", fields[i]: "link_count"})  # type: ignore
            #df_field["_field"] = fields[i]
            df_field.set_index("_time")

            logger.info(f"Dataframe of InfluxDB: {df_field}")

            # Push points to influxDB
            logger.info(f"[InfluxDB] Writing data to {db_net.influx_net}")
            write_api.write(bucket=settings.INFLUX_BUCKET,
                            org=settings.INFLUX_ORG,
                            record=df_field,
                            data_frame_measurement_name=db_net.influx_net,
                            data_frame_timestamp_column="_time",
                            data_frame_tag_columns=['interface'])
            logger.info(f"[InfluxDB] Dataframe writed to database.")

    # Return Status if success or error
    return Status(message="Adding test data..")
