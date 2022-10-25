from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "interfaces" ALTER COLUMN "influx_rx" SET NOT NULL;
        ALTER TABLE "interfaces" ALTER COLUMN "influx_tx" SET NOT NULL;
        ALTER TABLE "networks" ALTER COLUMN "influx_net" SET NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "networks" ALTER COLUMN "influx_net" DROP NOT NULL;
        ALTER TABLE "interfaces" ALTER COLUMN "influx_rx" DROP NOT NULL;
        ALTER TABLE "interfaces" ALTER COLUMN "influx_tx" DROP NOT NULL;"""
