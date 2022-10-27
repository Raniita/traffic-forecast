from datetime import datetime
from typing import List
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import WriteApi, WriteOptions, SYNCHRONOUS
from influxdb_client.client.delete_api import DeleteApi

from src.schemas.samples import Point
from src.main import logger
from src.config import settings

def connect_influx() -> InfluxDBClient:
    client = InfluxDBClient(url=settings.INFLUX_URL, token=settings.INFLUX_TOKEN)
    return client

def create_write_api() -> WriteApi:
    client = connect_influx()
    write_api = client.write_api(write_options=SYNCHRONOUS)
    return write_api

def create_delete_api() -> DeleteApi:
    client = connect_influx()
    delete_api = client.delete_api()
    return delete_api

def add_points(influx_network: str, influx_interface: str, point: List[Point]) -> str:
    write_api = create_write_api()
    
    points_list = []
    for p in point:
        points_list.append(Point(influx_network).tag("interface", influx_interface)
                                                .field("link-count", p.link_count)
                                                .time(p.timestamp, WritePrecision.S))
    try:
        write_api.write(bucket=settings.INFLUX_BUCKET,
                        org=settings.INFLUX_ORG,
                        record=points_list)

        logger.info("Succesfull writed samples on DB")
        return "OK"
    except Exception as ex:
        logger.info("Error writing samples on DB")
        logger.info(f"Exception: {ex}")
        return "KO"
        

def delete_network(influx_network: str):
    delete_api = create_delete_api()

    start = "1970-01-01T00:00:00Z"
    stop = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    delete_api.delete(start, stop, f'_measurement="{influx_network}"',
                      bucket=settings.INFLUX_BUCKET,
                      org=settings.INFLUX_ORG)

def delete_interface(influx_network: str, influx_interface: str):
    delete_api = create_delete_api()

    start = "1970-01-01T00:00:00Z"
    stop = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    delete_api.delete(start, stop, f'_measurement="{influx_network}" AND interface="{influx_interface}"',
                      bucket=settings.INFLUX_BUCKET,
                      org=settings.INFLUX_ORG)