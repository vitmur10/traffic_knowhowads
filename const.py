import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, types
from aiogram.fsm.storage.memory import MemoryStorage
load_dotenv()

API_TOKEN = os.getenv('TOKEN')
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
FILE_ID = "BAACAgIAAxkBAAMHZ-6YYKeVrN_QdIQMtKTTgxMasuMAAgJwAAJLHHBL55lkeWkCB8c2BA"  # Вставте отриманий file_id
DB_PATH = "users.db"
