from comand import *
from aiogram import F
from aiogram.filters import Command
from aiogram.types import FSInputFile
from const import *


# Запуск бота
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
