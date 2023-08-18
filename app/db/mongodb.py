import logging
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import MONGODB_URL


class MongoDB:
    client: AsyncIOMotorClient = None


mongodb = MongoDB()


async def get_mongodb() -> AsyncIOMotorClient:
    return mongodb.client


async def connect_to_mongo():
    logging.info("Connecting to mongodb")
    mongodb.client = AsyncIOMotorClient(str(MONGODB_URL))
    logging.info("Connecting to mongodb successfully")


async def close_mongo_connection():
    logging.info("Closing connections to mongodb")
    mongodb.client.close()
    logging.info("All connections with mongodb are closed")
