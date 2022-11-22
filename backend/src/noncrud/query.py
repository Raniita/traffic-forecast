from fastapi.responses import PlainTextResponse
from tortoise.exceptions import DoesNotExist, IntegrityError

from src.main import logger
from src.database.models import Networks, Interfaces
from src.schemas.networks import NetworkDatabaseSchema
from src.schemas.interfaces import InterfaceDatabaseSchema
from src.utils.influxdb import query_5m as influx_query_5m

async def query_linkcount_5m(id_network: str, id_interface: str, field: str, to_csv: bool):
    # Get influx fields of network and interface
    try:
        db_net = await NetworkDatabaseSchema.from_queryset_single(Networks.get(id_network=id_network))
    
        influx_network = db_net.influx_net
    except DoesNotExist:
        logger.info("Error. Network doesnt exists")
        raise DoesNotExist

    try:
        db_if = await InterfaceDatabaseSchema.from_queryset_single(Interfaces.get(network=db_net.id, id_interface=id_interface))
    
        if field.upper() == "RX":
            influx_interface = db_if.influx_rx
        elif field.upper() == "TX":
            influx_interface = db_if.influx_tx
        else:
            logger.info("Field not valid")
            raise DoesNotExist
    except DoesNotExist:
        logger.info("Error. Interface not found")
        raise DoesNotExist

    # Given a network and an interface, query:
    result_df = influx_query_5m(influx_network=influx_network,influx_interface=influx_interface)
    #logger.info(f"Result query: {result_df}")
    #logger.info(f"Type query result: {type(result_df)}")

    # Return data to client
    if to_csv:
        return PlainTextResponse(result_df.to_csv(index=False), media_type="text/csv")
    else:
        return PlainTextResponse(result_df.to_json(orient="index", date_format="iso"), media_type="application/json")
