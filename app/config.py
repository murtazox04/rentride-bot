from decouple import config

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = config("BOT_TOKEN")

bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)