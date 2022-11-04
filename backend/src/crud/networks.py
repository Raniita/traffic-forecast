from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist, IntegrityError

from src.database.models import Networks
from src.schemas.networks import NetworkOutSchema, NetworkInSchema, NetworkDatabaseSchema
from src.schemas.messages import Status
from src.utils.influxdb import create_network as influxdb_create_network
from src.utils.influxdb import delete_network as influxdb_delete_network

async def get_networks():
    return await NetworkOutSchema.from_queryset(Networks.all())

async def get_network(net_id) -> NetworkOutSchema:
    return await NetworkOutSchema.from_queryset_single(Networks.get(id_network=net_id))

async def create_network(net: NetworkInSchema) -> NetworkOutSchema:
    # net is a dict with network info given by user
    try:
        # Creating influxdb network measurement with dummy data
        influx_net = (str(net.id_network) + '-' + net.name).strip()
        influxdb_create_network(influx_net)

        net_obj = await Networks.create(**net.dict(exclude_unset=True), influx_net=influx_net)
    except IntegrityError:
        raise HTTPException(status_code=401, detail=f"That network ID already exists.")

    return await NetworkOutSchema.from_tortoise_orm(net_obj)

async def delete_network(net_id):
    # net_id is a integer for delete that network
    try:
        db_net = await NetworkDatabaseSchema.from_queryset_single(Networks.get(id_network=net_id))
    except DoesNotExist:
        raise HTTPException(status_code=401, detail=f"Network not found.")

    # Deleting influxdb measurement with all data
    influxdb_delete_network(db_net.influx_net)

    deleted_net = await Networks.filter(id_network=net_id).delete()
    if not deleted_net:
        raise HTTPException(status_code=404, detail=f"Network {net_id} not found")
    return Status(message=f"Deleted network {net_id}") 
    
async def update_network(net_id, net) -> NetworkOutSchema:
    try:
        db_net = await NetworkOutSchema.from_queryset_single(Networks.get(id_network=net_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Network {net_id} not found")

    await Networks.filter(id_network=net_id).update(**net.dict(exclude_unset=True))
    return await NetworkOutSchema.from_queryset_single(Networks.get(id_network=net_id))