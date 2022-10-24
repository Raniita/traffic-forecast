from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

import src.crud.networks as crud
from src.schemas.networks import NetworkInSchema, NetworkOutSchema

router = APIRouter()

@router.get('/networks', 
            response_model=List[NetworkOutSchema],
            tags=["Networks"])
async def get_networks():
    return await crud.get_networks()

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