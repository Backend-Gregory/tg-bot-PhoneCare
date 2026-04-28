import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN
from database import init_db
from handlers import router

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.include_router(router)

async def main():
    try:
        init_db()
        print("✅ База данных готова")
    except Exception as e:
        logging.error(f"Ошибка БД: {e}")
        return
    
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())