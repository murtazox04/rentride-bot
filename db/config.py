from decouple import config
from pydantic_settings import BaseSettings
from motor.motor_asyncio import AsyncIOMotorClient


class Settings(BaseSettings):
    mongodb_url: str = config("MONGODB_URL")
    mongodb_db: str = config("MONGODB_DB")


settings = Settings()


class MongoDB:
    client: AsyncIOMotorClient = None


db = MongoDB()


async def get_database() -> AsyncIOMotorClient:
    return db.client


async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.mongodb_url)


async def close_mongo_connection():
    db.client.close()
