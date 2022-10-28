from typing import List

from fastapi import APIRouter, HTTPException, Path
from fastapi_pagination import Page, paginate

from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

import src.crud.networks as crud
from src.schemas.networks import NetworkInSchema, NetworkOutSchema, UpdateNetwork
from src.schemas.messages import Status, HTTPUnauthorizedError


router = APIRouter()


@router.get('/networks', 
            response_model=Page[NetworkOutSchema],
            tags=["Networks"])
async def get_networks():
    """
    Return an item with all the networks:

    - **id_network**: Number for identificate a network
    - **name**: Name given to a network
    - **description**: Short description for the network
    - **ip_network**: IP of most important network monitored
    - **interfaces**: Returns alls interfaces associated with the network
    \f
    """
    
    result = await crud.get_networks()
    return paginate(result)


@router.post("/networks",
            response_model=NetworkOutSchema,
            responses={401: {"model": HTTPUnauthorizedError}},
            tags=["Networks"])
async def create_network(net: NetworkInSchema) -> NetworkOutSchema:
    """
    Create a network with all the informations:

    - **id_network**: Number for identificate a network
    - **name**: Name given to a network
    - **description**: Short description for the network
    - **ip_network**: IP of most important network monitored
    \f

    :param net: Network Schema for DataIn (id_net, name, description & ip_net)
    """

    return await crud.create_network(net)


@router.get('/networks/{network_id}', 
            response_model=NetworkOutSchema,
            responses={404: {"model": HTTPNotFoundError}},
            tags=["Networks"])
async def get_network(network_id: int = Path(None, description="ID of a monitored network")) -> NetworkOutSchema:
    """
    Return an item with the specified network:

    - **id_network**: Number for identificate a network
    - **name**: Name given to a network
    - **description**: Short description for the network
    - **ip_network**: IP of most important network monitored
    - **interfaces**: Returns alls interfaces associated with the network
    \f

    :param network_id: identifier for network
    """

    try:
        return await crud.get_network(network_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="Network does not exist."
        )


@router.patch("/networks/{network_id}",
              response_model=NetworkOutSchema,
              responses={404: {"model": HTTPNotFoundError}},
              tags=["Networks"])
async def update_network(net: UpdateNetwork,
                         network_id: int = Path(None, description="ID of a monitored network"),
                         ) -> NetworkOutSchema:
    """
    Update a network with information:

    - **name**: Name given to a network
    - **description**: Short description for the network
    - **ip_network**: IP of most important network monitored
    \f

    :param net: Item with updated info of the network
    :param network_id: identifier for network 
    """

    return await crud.update_network(net_id=network_id, net=net)


@router.delete("/networks/{network_id}",
               response_model=Status,
               responses={404: {"model": HTTPNotFoundError}},
               tags=["Networks"])
async def delete_network(network_id: int = Path(None, description="ID of a monitored network")):
    """
    Delete network given the id.
    \f

    :param network_id: identifier for network 
    """

    return await crud.delete_network(net_id=network_id)