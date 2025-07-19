from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_API_TOKEN, ADMINS
from aiogram.fsm.storage.memory import MemoryStorage

# admins = [int(admin_id) for admin_id in ADMINS.split(',')]
bot = Bot(token=BOT_API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(bot=bot, storage=MemoryStorage())