from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Networks

NetworkInSchema = pydantic_model_creator(
    Networks, name="NetworkIn", exclude_readonly=True
)

NetworkOutSchema = pydantic_model_creator(
    Networks, name="NetworkOut", exclude=("created_at", "modified_at")  
)

NetworkDatabaseSchema = pydantic_model_creator(
    Networks, name="NetworkOut", exclude=("created_at", "modified_at")  
)