from typing import List, Union

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

import src.noncrud.query as query


router = APIRouter(prefix="/query",
                   tags=["Query samples"])

@router.get("/", response_class=PlainTextResponse)
async def query_interface(network_id: str, 
                          interface_id: str, 
                          field: str,
                          csv: Union[bool, None] = None):
    """
        Query **monitored** data


    """

    return await query.query_linkcount_5m(id_network=network_id, id_interface=interface_id, field=field, to_csv=csv)