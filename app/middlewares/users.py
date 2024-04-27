import aiohttp
from aiogram.types import Message
from aiogram import BaseMiddleware
from decouple import config
from typing import Callable, Dict, Any, Awaitable

BASE_URL = config('BASE_URL')


class UserMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        if not await self.login(user_id):
            data = {
                "first_name": event.from_user.first_name,
                "last_name": event.from_user.last_name,
                "username": event.from_user.username,
            }
            await self.register_user(user_id, data)
        return await handler(event, data)

    async def login(self, user_id: int) -> bool:
        async with aiohttp.ClientSession() as session:
            response = await session.post(BASE_URL + "/login", json={"user_id": user_id})
            return response.status == 200

    async def register_user(self, user_id: int, data: Dict) -> None:
        async with aiohttp.ClientSession() as session:
            await session.post(BASE_URL + "/register", json={"user_id": user_id, **data})
