from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "interfaces" ADD "influx_rx" VARCHAR(30);
        ALTER TABLE "interfaces" ADD "influx_tx" VARCHAR(30);
        ALTER TABLE "networks" ADD "influx_net" VARCHAR(30);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "networks" DROP COLUMN "influx_net";
        ALTER TABLE "interfaces" DROP COLUMN "influx_rx";
        ALTER TABLE "interfaces" DROP COLUMN "influx_tx";"""
