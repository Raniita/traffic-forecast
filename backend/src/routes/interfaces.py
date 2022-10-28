from typing import List

from fastapi import APIRouter, HTTPException, Path
from fastapi_pagination import Page, paginate

from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

import src.crud.interfaces as crud
from src.schemas.interfaces import InterfaceInSchema, InterfaceOutSchema, UpdateInterface
from src.schemas.messages import Status, HTTPUnauthorizedError


router = APIRouter()


@router.get("/networks/{network_id}/interfaces",
            response_model=Page[InterfaceOutSchema],
            responses={401: {"model": HTTPNotFoundError}},
            tags=["Interfaces"])
async def get_interfaces(network_id: int = Path(None, description="ID of a monitored network")):
    """
    Return an item with all the interfaces:

    - **id_interface**: Number for identificate an interface
    - **name**: Name given to a network
    - **description**: Short description for the network
    - **network**: Object with all the information of the network
    \f

    :param network_id: identifier for network
    """
    
    result = await crud.get_interfaces(net_id=network_id)
    return paginate(result)


@router.post("/networks/{network_id}/interfaces",
             response_model=InterfaceOutSchema,
             responses={401: {"model": HTTPNotFoundError}},
             tags=["Interfaces"])
async def create_interface(inter: InterfaceInSchema, 
                           network_id: int = Path(None, description="ID of a monitored network")
                          ) -> InterfaceOutSchema:
    """
    Create an interface with all the informations:

    - **id_interface**: Number for identificate the interface
    - **name**: Name given to a network
    - **description**: Short description for the network
    \f

    :param inter: Interface Schema for DataIn (id_inter, name & description)
    :param network_id: identifier for network
    """

    return await crud.create_interface(interface=inter, net_id=network_id)


@router.get("/networks/{network_id}/interfaces/{interface_id}",
            response_model=InterfaceOutSchema,
            responses={401: {"model": HTTPNotFoundError}},
            tags=["Interfaces"])
async def get_interface(network_id: int = Path(None, description="ID of a monitored network"), 
                        interface_id: int = Path(None, description="ID of a monitored interface")):
    """
    Return an item with the specified interface:

    - **id_interface**: Number for identificate an interface
    - **name**: Name given to a network
    - **description**: Short description for the network
    - **network**: Object with all the information of the network
    \f

    :param network_id: identifier for network
    """

    return await crud.get_interface(if_id=interface_id, net_id=network_id)


@router.patch("/networks/{network_id}/interfaces/{interface_id}",
             response_model=InterfaceOutSchema,
             responses={404: {"model": HTTPNotFoundError},
                        401: {"model": HTTPUnauthorizedError}},
             tags=["Interfaces"])
async def update_interface(interface: UpdateInterface, 
                           network_id: int = Path(None, description="ID of a monitored network"), 
                           interface_id: int = Path(None, description="ID of a monitored interface")
                          ) -> InterfaceOutSchema:
    """
    Update a network with information:

    - **name**: Name given to a network
    - **description**: Short description for the network
    - **ip_network**: IP of most important network monitored
    \f

    :param net: Item with updated info of the network
    :param network_id: identifier for network 
    :param interface_id: identifier for interface 
    """

    return await crud.update_interface(net_id=network_id, if_id=interface_id, interface=interface)


@router.delete("/networks/{network_id}/interfaces/{interface_id}",
              response_model=Status,
              responses={404: {"model": HTTPNotFoundError},
                         401: {"model": HTTPUnauthorizedError}},
              tags=["Interfaces"])
async def delete_interface(network_id: int = Path(None, description="ID of a monitored network"), 
                           interface_id: int = Path(None, description="ID of a monitored interface")):
    """
    Delete interface given the id.
    \f

    :param network_id: identifier for network
    :param interface_id: identifier for interface  
    """

    return await crud.delete_interface(if_id=interface_id, net_id=network_id)