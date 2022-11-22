from typing import Optional

from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Networks

## TODO: revisar si necesario orm_mode
class pydantic_config:
    orm_mode = True

NetworkInSchema = pydantic_model_creator(
    Networks, name="NetworkIn", exclude=("id",
                                         "interfaces",
                                         "influx_net"),
                                         exclude_readonly=True
)

NetworkOutSchema = pydantic_model_creator(
    Networks, name="NetworkOut", exclude=("id",
                                          "influx_net",
                                          "created_at", 
                                          "modified_at", 
                                          "interfaces.id",
                                          "interfaces.influx_rx",
                                          "interfaces.influx_tx",
                                          "interfaces.created_at",
                                          "interfaces.modified_at")  
)

NetworkDatabaseSchema = pydantic_model_creator(
    Networks, name="NetworkDatabase"  
)

class NetworkInSchema(NetworkInSchema):
    class Config:
        schema_extra = {
            "example": {
                "id_network": "0",
                "name": "net-0",
                "description": "description here",
                "ip_network": "0.0.0.0",
            }
        }

class UpdateNetwork(BaseModel):
    name: Optional[str]
    description: Optional[str] 
    ip_network: Optional[str]