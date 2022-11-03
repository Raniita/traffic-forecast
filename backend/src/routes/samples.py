from typing import List

from fastapi import APIRouter

import src.noncrud.samples as samples

router = APIRouter(prefix="/samples",
                   tags=["Samples"])


@router.get("/test_data")
async def add_test_data():
    return await samples.add_test_data()