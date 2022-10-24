from typing import List

from fastapi import APIRouter, HTTPException

from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

import src.crud.interfaces as crud
from src.schemas.interfaces import InterfaceInSchema, InterfaceOutSchema
from src.schemas.messages import Status


router = APIRouter()


@router.get("/networks/{net_id}/interfaces",
            response_model=List[InterfaceOutSchema],
            tags=["Interfaces"])
async def get_interfaces(net_id: int):
    return await crud.get_interfaces(net_id=net_id)


@router.post("/networks/{net_id}/interfaces",
             response_model=InterfaceOutSchema,
             tags=["Interfaces"])
async def create_interface(inter: InterfaceInSchema, net_id: int) -> InterfaceOutSchema:
    return await crud.create_interface(interface=inter, net_id=net_id)


@router.get("/networks/{net_id}/interfaces/{inter_id}",
            response_model=InterfaceOutSchema,
            tags=["Interfaces"])
async def get_interface(net_id: int, inter_id: int):
    return await crud.get_interface(if_id=inter_id, net_id=net_id)


@router.patch("/networks/{net_id}/interfaces/{inter_id}",
             response_model=InterfaceOutSchema,
             responses={404: {"model": HTTPNotFoundError}},
             tags=["Interfaces"])
async def update_interface(net_id: int, inter_id: int, inter: InterfaceInSchema):
    return await crud.update_interface(net_id=net_id, if_id=inter_id, interface=inter)


@router.delete("/networks/{net_id}/interfaces/{inter_id}",
              response_model=Status,
              responses={404: {"model": HTTPNotFoundError}},
              tags=["Interfaces"])
async def delete_interface(net_id: int, inter_id: int):
    return await crud.delete_interface(if_id=inter_id, net_id=net_id)