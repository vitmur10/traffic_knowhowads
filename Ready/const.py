import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, types
from aiogram.fsm.storage.memory import MemoryStorage
load_dotenv()

API_TOKEN = os.getenv('TOKEN_READY')
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
FILE_ID = "BAACAgIAAxkBAAMLaAPPpIX4cFaG8Cusc5n4EPdEFDcAAnJ3AALl-iBIVHq8Tpn4tzQ2BA"  # Вставте отриманий file_id
DB_PATH = "users_ready.db"
