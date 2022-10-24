from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "networks" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "id_network" BIGINT NOT NULL UNIQUE,
    "name" VARCHAR(100),
    "description" VARCHAR(100),
    "ip_network" VARCHAR(20) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "interfaces" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "id_interface" BIGINT NOT NULL UNIQUE,
    "name" VARCHAR(100),
    "description" VARCHAR(100),
    "network_id" BIGINT NOT NULL REFERENCES "networks" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
