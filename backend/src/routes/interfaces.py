from typing import List

from fastapi import APIRouter, HTTPException

from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

import src.crud.interfaces as crud
from src.schemas.interfaces import InterfaceInSchema, InterfaceOutSchema, UpdateInterface
from src.schemas.messages import Status


router = APIRouter()


@router.get("/networks/{network_id}/interfaces",
            response_model=List[InterfaceOutSchema],
            tags=["Interfaces"])
async def get_interfaces(network_id: int):
    return await crud.get_interfaces(net_id=network_id)


@router.post("/networks/{network_id}/interfaces",
             response_model=InterfaceOutSchema,
             tags=["Interfaces"])
async def create_interface(inter: InterfaceInSchema, network_id: int) -> InterfaceOutSchema:
    return await crud.create_interface(interface=inter, net_id=network_id)


@router.get("/networks/{network_id}/interfaces/{interface_id}",
            response_model=InterfaceOutSchema,
            tags=["Interfaces"])
async def get_interface(network_id: int, interface_id: int):
    return await crud.get_interface(if_id=interface_id, net_id=network_id)


@router.patch("/networks/{network_id}/interfaces/{interface_id}",
             response_model=InterfaceOutSchema,
             responses={404: {"model": HTTPNotFoundError}},
             tags=["Interfaces"])
async def update_interface(network_id: int, interface_id: int, interface: UpdateInterface):
    return await crud.update_interface(net_id=network_id, if_id=interface_id, interface=interface)


@router.delete("/networks/{network_id}/interfaces/{interface_id}",
              response_model=Status,
              responses={404: {"model": HTTPNotFoundError}},
              tags=["Interfaces"])
async def delete_interface(network_id: int, interface_id: int):
    return await crud.delete_interface(if_id=interface_id, net_id=network_id)