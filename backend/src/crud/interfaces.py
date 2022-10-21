from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist, IntegrityError

from src.database.models import Interfaces, Networks
from src.schemas.interfaces import InterfaceOutSchema
from src.schemas.networks import NetworkOutSchema

async def get_interfaces(net_id):
    return await InterfaceOutSchema.from_queryset(Interfaces.filter(net=net_id))

async def get_interface(if_id, net_id) -> InterfaceOutSchema:
    return await InterfaceOutSchema.from_queryset_single(Interfaces.filter(net=net_id).get(id_if=if_id))

async def create_interface(interface) -> InterfaceOutSchema:
    # check if network exists
    try:
        db_net = await NetworkOutSchema.from_queryset_single(Networks.get(id_net=interface.net))
    except DoesNotExist:
        raise HTTPException(status_code=401, detail=f"Network ID {interface.net} doesnt exists.")

    try:
        if_obj = await Interfaces.create(**interface.dict(exclude_unset=True))
    except IntegrityError:
        raise HTTPException(status_code=401, detail=f"That interface ID already exists")

    return await InterfaceOutSchema.from_tortoise_orm(if_obj)

async def delete_interface(if_id, net_id):
    try:
        db_net = await NetworkOutSchema.from_queryset_single(Networks.get(id_net=net_id))
    except DoesNotExist:
        raise HTTPException(status_code=401, detail=f"Network ID {net_id} doesnt exists.")

    deleted_interface = await Interfaces.filter(if_id).delete()
    if not deleted_interface:
        raise HTTPException(status_code=404, detail=f"Interface ID {if_id} not found.")
    return f"Deleted interface {if_id}"

async def update_interface(if_id, interface) -> InterfaceOutSchema:
    # TODO
    return InterfaceOutSchema.from_queryset_single(Interfaces.get(id_if=if_id))
