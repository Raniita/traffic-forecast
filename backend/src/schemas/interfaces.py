from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Interfaces

InterfaceInSchema = pydantic_model_creator(
    Interfaces, name="InterfaceIn", exclude=("id", 
                                             "network_id",
                                             "influx_rx",
                                             "influx_tx"), 
                                             exclude_readonly=True
)

InterfaceOutSchema = pydantic_model_creator(
    Interfaces, name="InterfaceOut", exclude=("id", 
                                              "created_at", 
                                              "modified_at",
                                              "influx_rx",
                                              "influx_tx", 
                                              "network.id",
                                              "network.influx_net",
                                              "network.created_at",
                                              "network.modified_at")
)

InterfaceDatabaseSchema = pydantic_model_creator(
    Interfaces, name="InterfaceDatabase",
)

class InterfaceInSchema(InterfaceInSchema):
    class Config:
        schema_extra = {
            "example": {
                "id_interface": "0",
                "name": "if-0",
                "description": "description here",
            }
        }

class UpdateInterface(BaseModel):
    name: Optional[str]
    description: Optional[str]