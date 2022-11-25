import pandas as pd
import random
from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist, IntegrityError

from src.main import logger
from src.config import settings
from src.database.models import Networks, Interfaces
from src.schemas.networks import NetworkDatabaseSchema
from src.schemas.interfaces import InterfaceDatabaseSchema
from src.schemas.messages import Status
from src.utils.influxdb import check_exists_network as influxdb_exists_network
from src.utils.influxdb import create_write_api as influxdb_create_write_api

async def import_topology(network_id: str, file):
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
            df_field["interface"] = interface_influx[i]
            df_field = df_field.rename(columns={"timestamp": "_time", fields[i]: "link_count"})  # type: ignore
            df_field.set_index("_time")

            #logger.info(f"Dataframe of InfluxDB: {df_field}")

            # Push points to influxDB
            logger.info(f"[InfluxDB] Writing data to {db_net.influx_net}")
            write_api.write(bucket=settings.INFLUX_BUCKET,
                            org=settings.INFLUX_ORG,
                            record=df_field,
                            data_frame_measurement_name=db_net.influx_net,
                            data_frame_timestamp_column="_time",
                            data_frame_timestamp_timezone="Europe/Madrid",
                            data_frame_tag_columns=['interface'])
            logger.info(f"[InfluxDB] Dataframe writed to database.")

    # Return Status if success or error
    return Status(message=f"Succesfully imported monitored data of topology on network {network_id}")


async def import_interface(network_id: str, interface_id: str, field: str, file):
    # Verify that network exists
    try:
        db_net = await NetworkDatabaseSchema.from_queryset_single(Networks.get(id_network=network_id))
    except DoesNotExist:
        raise HTTPException(status_code=401, detail=f"Network ID not found.")

    # Verify that influxdb networks exists
    if influxdb_exists_network(influx_network=db_net.influx_net):
        logger.info("Network exists")
    else:
        raise HTTPException(status_code=401, detail=f"Network not found on database.")

    # Verify that interface exists
    try:
        db_if = await InterfaceDatabaseSchema.from_queryset_single(Interfaces.get(network=db_net.id, id_interface=interface_id))
    
        if field.upper() == "RX":
            influx_interface = db_if.influx_rx
        elif field.upper() == "TX":
            influx_interface = db_if.influx_tx
        else:
            logger.info("Field not valid")
            raise HTTPException(status_code=401, detail=f"Interface field invalid. User 'rx' or 'tx'")
    except DoesNotExist:
        raise HTTPException(status_code=401, detail=f"Interface ID {interface_id} doesnt exists.")

    # Import to pandas
    df = pd.read_csv(file)
    logger.info(f"Dataframe upload: {df}")

    write_api = influxdb_create_write_api()

    # Interface must be created before!
    logger.info(f"Field: {field}")
    df_field = df[["time", "flow"]]

    # Adapt dataframe to InfluxDB format
    df_field["interface"] = influx_interface
    df_field = df_field.rename(columns={"time": "_time", "flow": "link_count"})  # type: ignore
    #df_field["_time"] = df_field["_time"].tz_convert('Europe/Madrid')
    df_field.set_index("_time")

    logger.info(f"Dataframe of InfluxDB: {df_field}")

    # Push points to influxDB
    logger.info(f"[InfluxDB] Writing data to {db_net.influx_net}")
    write_api.write(bucket=settings.INFLUX_BUCKET,
                    org=settings.INFLUX_ORG,
                    record=df_field,
                    data_frame_measurement_name=db_net.influx_net,
                    data_frame_timestamp_column="_time",
                    #data_frame_timestamp_timezone="UTC",
                    data_frame_tag_columns=['interface'])
    logger.info(f"[InfluxDB] Dataframe writed to database.")

    return Status(message=f"Succesfully imported monitored data on interface {interface_id} with mode: {field}")
