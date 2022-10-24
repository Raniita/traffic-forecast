from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

import src.crud.networks as crud
from src.schemas.networks import NetworkInSchema, NetworkOutSchema
from src.schemas.messages import Status


router = APIRouter()


@router.get('/networks', 
            response_model=List[NetworkOutSchema],
            tags=["Networks"])
async def get_networks():
    return await crud.get_networks()


@router.post("/networks",
            response_model=NetworkOutSchema,
            tags=["Networks"]
            )
async def create_network(net: NetworkInSchema) -> NetworkOutSchema:
    return await crud.create_network(net)


@router.get('/networks/{net_id}', 
            response_model=NetworkOutSchema,
            tags=["Networks"])
async def get_network(net_id: int) -> NetworkOutSchema:
    try:
        return await crud.get_network(net_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Network does not exist."
        )


@router.patch("/networks/{net_id}",
              response_model=NetworkOutSchema,
              responses={404: {"model": HTTPNotFoundError}},
              tags=["Networks"])
async def update_network(net_id: int,
                        net: NetworkInSchema) -> NetworkOutSchema:
    return await crud.update_network(net_id=net_id, net=net)


@router.delete("/networks/{net_id}",
               response_model=Status,
               responses={404: {"model": HTTPNotFoundError}},
               tags=["Networks"])
async def delete_network(net_id: int):
    return await crud.delete_network(net_id=net_id)