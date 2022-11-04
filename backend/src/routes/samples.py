from typing import List

from fastapi import APIRouter, File, UploadFile

import src.noncrud.samples as samples

router = APIRouter(prefix="/samples",
                   tags=["Samples"])


@router.post("/{network_id}/test_data")
async def add_test_data(network_id: str, file: UploadFile):
    """
        Upload a **.CSV** to insert the data on the relating network.

        CSV columns:
        - **timestamp**: timestamp with ISO format
        - **interface**: interface name of the entry
        - **TX**: link count for transmited dataframes on the interface
        - **RX**: link count for receive dataframes on the interface
    """

    return await samples.add_test_data(network_id=network_id, file=file.file)