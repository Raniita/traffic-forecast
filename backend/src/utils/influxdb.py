from datetime import datetime
from typing import List
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.rest import ApiException
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

def check_influxdb() -> None:
    client = connect_influx()
    
    health = client.health()
    if health.status == "pass":
        logger.info("Influxdb connection SUCCESS.")
    else:
        logger.warn(f"Influxdb connection FAILURE: {health.message}!")

def check_query() -> None:
    try:
        client = connect_influx()
        client.query_api().query(f"from(bucket:\"{settings.INFLUX_BUCKET}\") |> range(start: -1m) |> limit(n:1)", settings.INFLUX_ORG)
    except ApiException as e:
        if e.status == 404:
            raise Exception(f"The specified token doesn't have sufficient credentials to read from '{settings.INFLUX_BUCKET}' "
                            f"or specified bucket doesn't exists.") from e
        raise

def check_write() -> None:
    try:
        client = connect_influx()
        client.write_api(write_options=SYNCHRONOUS).write(settings.INFLUX_BUCKET, settings.INFLUX_ORG, b"")
    except ApiException as e:
        # bucket does not exist
        if e.status == 404:
            raise Exception(f"The specified bucket does not exist.") from e
        # insufficient permissions
        if e.status == 403:
            raise Exception(f"The specified token does not have sufficient credentials to write to '{settings.INFLUX_BUCKET}'.") from e
        # 400 (BadRequest) caused by empty LineProtocol
        if e.status != 400:
            raise

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