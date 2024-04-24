from aiogram import Dispatcher, types

from middlewares import UserMiddleware
from loader import app, dp, bot, WEBHOOK_PATH, WEBHOOK_URL


@app.on_event("startup")
async def on_startup() -> None:
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
    await dp.storage.close()
