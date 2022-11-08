from typing import List, Union

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

import src.noncrud.query as query


router = APIRouter(prefix="/query",
                   tags=["Query samples"])

@router.get("/", response_class=PlainTextResponse)
async def query_interface(network_id: str, 
                          interface_id: str, 
                          field: str = "RX",
                          to_csv: Union[bool, None] = False):
    """
        Query **monitored** data. Parameters:

        - **network_id**: Number for identificate a network
        - **interface_id**: Number for identificate an interface
        - **field**: Select over **RX** or **TX** 
        - **csv**: If true, the response will be a csv, if not, the response will be a json

    """

    return await query.query_linkcount_5m(id_network=network_id, id_interface=interface_id, field=field, to_csv=to_csv)