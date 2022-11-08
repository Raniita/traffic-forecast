from datetime import datetime
from typing import List
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.rest import ApiException
from influxdb_client.client.query_api import QueryApi
from influxdb_client.client.write_api import WriteApi, WriteOptions, SYNCHRONOUS
from influxdb_client.client.delete_api import DeleteApi
from tortoise.exceptions import DoesNotExist, IntegrityError

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


def create_query_api() -> QueryApi:
    client = connect_influx()
    query_api = client.query_api()
    return query_api


def check_influxdb() -> None:
    client = connect_influx()
    
    health = client.health()
    if health.status == "pass":
        logger.info("[InfluxDB] Connection SUCCESS.")
    else:
        logger.warn(f"[InfluxDB] Connection FAILURE: {health.message}!")


def check_query() -> None:
    try:
        client = connect_influx()
        client.query_api().query(f"from(bucket:\"{settings.INFLUX_BUCKET}\") |> range(start: -1m) |> limit(n:1)", settings.INFLUX_ORG)
    except ApiException as e:
        if e.status == 404:
            raise Exception(f"The specified token doesn't have sufficient credentials to read from '{settings.INFLUX_BUCKET}' "
                            f"or specified bucket doesn't exists.") from e
        raise

    logger.info("[InfluxDB] Selftest read access SUCCESS")


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

    logger.info("[InfluxDB] Selftest write access SUCCESS")


def create_network(influx_network: str):
    logger.info(f"[InfluxDB] Creating network {influx_network}")
    write_api = create_write_api()
    now = int(datetime.now().timestamp())

    init_point = Point(influx_network).tag("interface", "init-if").field("link_count", 0).time(now, WritePrecision.S)

    try:
        write_api.write(bucket=settings.INFLUX_BUCKET,
                        org=settings.INFLUX_ORG,
                        record=[init_point])
        logger.info(f"[InfluxDB] Succesfull created network {influx_network}")
        return "OK"
    except Exception as ex:
        logger.info("[InfluxDB] Error writing samples to database")
        logger.info(f"[InfluxDB] Exception: {ex}")
        return "KO"


def check_exists_network(influx_network: str) -> bool:
    logger.info(f"[InfluxDB] Verify if network {influx_network} exists")
    try:
        query_api = create_query_api()
    
        query = f'from(bucket: "{settings.INFLUX_BUCKET}")' \
                    ' |> range(start: 1970-01-01T00:00:00Z)' \
                   f' |> filter(fn: (r) => r["_measurement"] == "{influx_network}")'
        #logger.info(f"[InfluxDB] Query: {query}")

        result = query_api.query(query, settings.INFLUX_ORG)
        #logger.info(f"[InfluxDB] Result of query: {type(result)}")
        if result:
            logger.info(f"[InfluxDB] Network already exists")
            return True
        else:
            logger.info(f"[InfluxDB] Network doesnt exists")
            return False
    except ApiException as ex:
        logger.warn(f"[InfluxDB] Error ex: {ex}")
        return False


def delete_network(influx_network: str):
    logger.info(f"[InfluxDB] Deleting network {influx_network}")
    delete_api = create_delete_api()

    start = "1970-01-01T00:00:00Z"
    stop = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        delete_api.delete(start, stop, f'_measurement="{influx_network}"',
                        bucket=settings.INFLUX_BUCKET,
                        org=settings.INFLUX_ORG)
        logger.info(f"[InfluxDB] Succesfull deleted network {influx_network}")
    except Exception as ex:
        logger.info("[InfluxDB] Error writing samples to database")
        logger.info(f"[InfluxDB] Exception: {ex}")


def delete_interface(influx_network: str, influx_interface: str):
    delete_api = create_delete_api()

    start = "1970-01-01T00:00:00Z"
    stop = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    delete_api.delete(start, stop, f'_measurement="{influx_network}" AND interface="{influx_interface}"',
                      bucket=settings.INFLUX_BUCKET,
                      org=settings.INFLUX_ORG)


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
        

def query_5m(influx_network: str, influx_interface: str):
    try:
        client = connect_influx()

        query = f'from(bucket: "{settings.INFLUX_BUCKET}")' \
                    ' |> range(start: 1970-01-01T00:00:00Z)' \
                   f' |> filter(fn: (r) => r["_measurement"] == "{influx_network}")' \
                    ' |> filter(fn: (r) => r["_field"] == "link_count")' \
                   f' |> filter(fn: (r) => r["interface"] == "{influx_interface}")' \
                    ' |> aggregateWindow(every: 5m, fn: mean, createEmpty: false)' \
                    ' |> yield(name: "mean")' \
                    #' |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'    

        #logger.info(f"Query: {query}")

        df_result = client.query_api().query_data_frame(query, settings.INFLUX_ORG)
        #logger.info(f"Result query: {df_result}")
        #logger.info(f"Type result: {type(df_result)}")
        
        if not df_result.empty:
            df_result = remove_columns_result_query(df_result)
            return df_result
        else:
            raise DoesNotExist
    except ApiException as e:
        if e.status == 404:
            raise Exception(f"The specified token doesn't have sufficient credentials to read from '{settings.INFLUX_BUCKET}' "
                            f"or specified bucket doesn't exists.") from e
        raise

def remove_columns_result_query(df):
    df = df.drop(columns=['result', 'table', '_start', '_stop', '_measurement'])
    df = df.rename(columns={'_time': 'time', '_value': 'value', '_field': 'field'})
    return df