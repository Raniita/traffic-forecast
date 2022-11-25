from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist, IntegrityError

from src.database.models import Interfaces, Networks
from src.schemas.interfaces import InterfaceOutSchema, InterfaceDatabaseSchema
from src.schemas.networks import NetworkOutSchema, NetworkDatabaseSchema
from src.schemas.messages import Status
from src.main import logger
from src.utils.influxdb import delete_interface as influxdb_delete_interface

async def get_interfaces(net_id):
    try:
        db_net = await NetworkDatabaseSchema.from_queryset_single(Networks.get(id_network=net_id))
    except DoesNotExist:
        raise HTTPException(status_code=401, detail=f"Network ID {net_id} doesnt exists.")

    return await InterfaceOutSchema.from_queryset(Interfaces.filter(network_id=db_net.id))

async def get_interface(if_id, net_id) -> InterfaceOutSchema:
    try:
        db_net = await NetworkDatabaseSchema.from_queryset_single(Networks.get(id_network=net_id))
    except DoesNotExist:
        raise HTTPException(status_code=401, detail=f"Network ID {net_id} doesnt exists.")

    return await InterfaceOutSchema.from_queryset_single(Interfaces.filter(network=db_net.id).get(id_interface=if_id))

async def create_interface(interface, net_id) -> InterfaceOutSchema:
    # check if network exists
    try:
        db_net = await NetworkDatabaseSchema.from_queryset_single(Networks.get(id_network=net_id))
    except DoesNotExist:
        raise HTTPException(status_code=401, detail=f"Network ID {interface.net} doesnt exists.")

    try:
        influx_rx = (str(interface.id_interface) + '-' + interface.name + '-RX').strip()
        influx_tx = (str(interface.id_interface) + '-' + interface.name + '-TX').strip()
        if_obj = await Interfaces.create(**interface.dict(), network_id=db_net.id,
                                                             influx_rx=influx_rx,
                                                             influx_tx=influx_tx)
    except IntegrityError:
        raise HTTPException(status_code=401, detail=f"That interface ID already exists.")
    except DoesNotExist:
        raise HTTPException(status_code=401, detail=f"Some fields doesnt exists.")

    return await InterfaceOutSchema.from_tortoise_orm(if_obj)

async def delete_interface(if_id, net_id):
    try:
        db_net = await NetworkDatabaseSchema.from_queryset_single(Networks.get(id_network=net_id))
    except DoesNotExist:
        raise HTTPException(status_code=401, detail=f"Network ID {net_id} doesnt exists.")

    try:
        db_if = await InterfaceDatabaseSchema.from_queryset_single(Interfaces.get(network=db_net.id, id_interface=if_id))
    except DoesNotExist:
        raise HTTPException(status_code=401, detail=f"Interface ID {if_id} doesnt exists.")

    deleted_interface = await Interfaces.filter(id_interface=if_id, network=db_net.id).delete()
    if not deleted_interface:
        raise HTTPException(status_code=404, detail=f"Interface ID {if_id} not found.")

    # Delete interface on influxdb
    influxdb_delete_interface(db_net.influx_net, db_if.influx_rx)
    influxdb_delete_interface(db_net.influx_net, db_if.influx_tx)

    return Status(message=f"Deleted interface with ID {if_id}")

async def update_interface(net_id, if_id, interface) -> InterfaceOutSchema:
    try:
        db_net = await NetworkDatabaseSchema.from_queryset_single(Networks.get(id_network=net_id))
    except DoesNotExist:
        raise HTTPException(status_code=401, detail=f"Network ID {net_id} doesnt exists.")
    
    try:
        db_if = await InterfaceDatabaseSchema.from_queryset_single(Interfaces.get(network=db_net.id, id_interface=if_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Interface {if_id} not found.")
    
    await Interfaces.filter(network=db_net.id, id_interface=if_id).update(**interface.dict(exclude_unset=True), network_id=db_net.id)
    return await InterfaceOutSchema.from_queryset_single(Interfaces.filter(network=db_net.id).get(id_interface=if_id))
