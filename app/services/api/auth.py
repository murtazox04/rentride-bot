import aiohttp
from typing import Optional

from db.service import DBService


class UserAuthService:
    def __init__(self, api_url: str, db: DBService, session: Optional[aiohttp.ClientSession] = None):
        self.api_url = api_url
        self.db = db
        self.session = session or aiohttp.ClientSession()

    async def register(self, username: str, password: str) -> str:
        resp = await self.session.post(
            f"{self.api_url}/register",
            json={"username": username, "password": password},
        )
        data = await resp.json()
        access_token = data["access_token"]
        refresh_token = data["refresh_token"]

        # Store the user in the database
        await self.db.create_user({
            "username": username,
            "access_token": access_token,
            "refresh_token": refresh_token,
        })

        return access_token

    async def login(self, username: str, password: str) -> str:
        resp = await self.session.post(
            f"{self.api_url}/login",
            json={"username": username, "password": password},
        )
        data = await resp.json()
        access_token = data["access_token"]
        refresh_token = data["refresh_token"]

        # Update the user's tokens in the database
        await self.db.update_user(username, {
            "access_token": access_token,
            "refresh_token": refresh_token,
        })

        return access_token
