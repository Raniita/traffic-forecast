from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Interfaces

InterfaceInSchema = pydantic_model_creator(
    Interfaces, name="InterfaceIn", exclude=("id_net", ""), exclude_readonly=True
)

InterfaceOutSchema = pydantic_model_creator(
    Interfaces, name="InterfaceOut", exclude=("created_at", "modified_at")
)

InterfaceDatabaseSchema = pydantic_model_creator(
    Interfaces, name="InterfaceOut", exclude=("created_at", "modified_at")
)