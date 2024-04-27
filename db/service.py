from typing import Optional
from pymongo import MongoClient
from pymongo.collection import Collection


class DBService:
    def __init__(self, db: MongoClient, collection_name: str):
        self.collection: Collection = db[collection_name]

    async def create_user(self, user_data: dict) -> dict:
        result = await self.collection.insert_one(user_data)
        return {"_id": str(result.inserted_id)}

    async def get_user(self, username: str) -> Optional[dict]:
        user = await self.collection.find_one({"username": username})
        if user:
            user["_id"] = str(user["_id"])
        return user

    async def update_user(self, username: str, user_data: dict) -> Optional[dict]:
        result = await self.collection.update_one({"username": username}, {"$set": user_data})
        if result.modified_count:
            return await self.get_user(username)

    async def delete_user(self, username: str) -> dict:
        result = await self.collection.delete_one({"username": username})
        return {"deleted_count": result.deleted_count}
