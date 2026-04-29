import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ErrorEvent

from config import TOKEN, ADMIN_ID
from database import init_db
from handlers import router
from middlewares import RateLimitMiddleware

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.message.middleware(RateLimitMiddleware(interval=1))
dp.include_router(router)

@dp.errors()
async def global_error_handler(event: ErrorEvent):
    logging.error(f"🔥 Глобальная ошибка: {event.exception}")
    try:
        await bot.send_message(ADMIN_ID, f"⚠️ Ошибка в боте:\n{event.exception}")
    except:
        pass
    return True

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