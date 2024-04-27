from aiogram import Dispatcher, types

from app.config import dp, bot
from app.middlewares import UserMiddleware
from loader import app, WEBHOOK_URL, WEBHOOK_PATH
from db.config import connect_to_mongo, close_mongo_connection


@app.on_event("startup")
async def on_startup() -> None:
    await connect_to_mongo()
    dp.message.middleware(UserMiddleware())
    # dp.include_router(callback_query_router)
    # dp.include_router(command_router)
    url = await bot.get_webhook_info()

    if url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict) -> None:
    telegram_update = types.Update(**update)
    await Dispatcher._feed_webhook_update(
        self=dp,
        bot=bot,
        update=telegram_update
    )


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await close_mongo_connection()
    await dp.storage.close()
