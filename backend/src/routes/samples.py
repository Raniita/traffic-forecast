from typing import List

from fastapi import APIRouter, UploadFile

import src.noncrud.samples as samples
from src.schemas.messages import Status

router = APIRouter(prefix="/samples",
                   tags=["Samples"])


@router.post("/{network_id}/import_topology")
async def import_topology(network_id: str, file: UploadFile) -> Status:
    """
        Upload a **.CSV** to insert the data on the relating network.

        Allow more than one interface

        CSV columns:
        - **timestamp**: timestamp with ISO format
        - **interface**: interface name of the entry
        - **TX**: link count for transmited dataframes on the interface
        - **RX**: link count for receive dataframes on the interface
    """

    return await samples.import_topology(network_id=network_id, file=file.file)


@router.post("/{network_id}/import_interface/{interface_id}") 
async def import_interface(network_id: str, interface_id:str, file: UploadFile, field: str = "RX") -> Status:
    """
        Upload a **.CSV** to insert data on the desired interface
    
        CSV columns:
        - **time**: datetime (iso format) of the point
        - **flow**: link count value
    """

    return await samples.import_interface(network_id=network_id, interface_id=interface_id, field=field, file=file.file)