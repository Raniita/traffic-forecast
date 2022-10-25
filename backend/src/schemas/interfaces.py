from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Interfaces

InterfaceInSchema = pydantic_model_creator(
    Interfaces, name="InterfaceIn", exclude=("id", "network_id"), exclude_readonly=True
)

InterfaceOutSchema = pydantic_model_creator(
    Interfaces, name="InterfaceOut", exclude=("id", "created_at", "modified_at")
)

InterfaceDatabaseSchema = pydantic_model_creator(
    Interfaces, name="InterfaceDatabase",
)

class UpdateInterface(BaseModel):
    name: Optional[str]
    description: Optional[str]