import asyncio
import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

# --- Конфигурация ---
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
WEBHOOK_PATH = "/webhook"
BASE_URL = os.getenv("RENDER_EXTERNAL_URL", "https://your-app.onrender.com")  # Render подставит сам
WEBHOOK_URL = f"{BASE_URL}{WEBHOOK_PATH}"

# --- Логирование ---
logging.basicConfig(level=logging.INFO)

# --- Инициализация бота ---
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# --- Клавиатура выбора услуг ---
service_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Замена экрана'), KeyboardButton(text='Замена аккумулятора')],
        [KeyboardButton(text='Диагностика'), KeyboardButton(text='Ремонт кнопок')]
    ],
    resize_keyboard=True
)

# --- Главная клавиатура ---
kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='📞 Контакты'), KeyboardButton(text='💼 Услуги')],
        [KeyboardButton(text='💰 Цены'), KeyboardButton(text='📍 Адрес')],
        [KeyboardButton(text='❓ Помощь')],
        [KeyboardButton(text='📝 Записаться')]
    ],
    resize_keyboard=True
)

# --- FSM состояния ---
class OrderForm(StatesGroup):
    service = State()
    master = State()
    name = State()
    phone = State()
    time = State()

# --- Мастера ---
masters = {
    "Замена экрана": ["Антон", "Дмитрий"],
    "Замена аккумулятора": ["Антон", "Сергей"],
    "Диагностика": ["Сергей"],
    "Ремонт кнопок": ["Антон", "Дмитрий"]
}

# --- Хендлеры ---
@dp.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Привет! Я бот мастерской PhoneCare.\n"
        "Отремонтируем твой телефон быстро и недорого.\n"
        "Выбери нужный раздел на кнопках ниже 👇",
        reply_markup=kb
    )

@dp.message(lambda message: message.text == '📝 Записаться')
async def start_order(message: types.Message, state: FSMContext):
    await state.set_state(OrderForm.name)
    await message.answer('Как тебя зовут?', reply_markup=ReplyKeyboardRemove())

@dp.message(OrderForm.name)
async def get_name(message: types.Message, state: FSMContext):
    if not message.text or not message.text.strip():
        await message.answer('Введите текст')
        return
    if len(message.text) > 100:
        await message.answer("❌ Слишком длинное имя")
        return
    await state.update_data(name=message.text)
    await state.set_state(OrderForm.phone)
    await message.answer('Какой номер телефона?')

@dp.message(OrderForm.phone)
async def get_phone(message: types.Message, state: FSMContext):
    if not message.text or not message.text.strip():
        await message.answer('Введите текст')
        return
    if len(message.text) > 100:
        await message.answer("❌ Слишком длинный телефон")
        return
    await state.update_data(phone=message.text)
    data = await state.get_data()
    
    try:
        await bot.send_message(
            ADMIN_ID,
            f"📝 Новая заявка!\nИмя: {data.get('name')}\nТелефон: {data.get('phone')}"
        )
        await message.answer('✅ Спасибо! Мы свяжемся с вами.', reply_markup=kb)
        await state.clear()
    except Exception as e:
        logging.error(f"Ошибка отправки админу: {e}")
        await message.answer("❌ Техническая ошибка. Попробуйте позже.", reply_markup=kb)

@dp.message(Command('cancel'))
async def cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('Опрос отменён', reply_markup=kb)

@dp.message()
async def handle_menu(message: types.Message):
    if message.text == '📞 Контакты':
        await message.answer('Телефон: +7 (999) 123-45-67\nTelegram: @phonecare\nВремя работы: 10:00–20:00')
    elif message.text == '💼 Услуги':
        await message.answer('• Замена экрана\n• Замена аккумулятора\n• Диагностика\n• Ремонт кнопок')
    elif message.text == '💰 Цены':
        await message.answer('• Замена экрана — от 2000₽\n• Аккумулятор — от 1500₽\n• Диагностика — 500₽ (бесплатно при ремонте)')
    elif message.text == '📍 Адрес':
        await message.answer('📍 г. Москва, ул. Строителей, д. 15\n🚇 м. Фрунзенская, выход к рынку')
    elif message.text == '❓ Помощь':
        await message.answer('📌 Используй кнопки меню.\nПо вопросам пиши @phonecare')
    else:
        await message.answer('Используй кнопки.', reply_markup=kb)

# --- Настройка webhook при запуске FastAPI ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook установлен: {WEBHOOK_URL}")
    yield
    await bot.delete_webhook()
    await bot.session.close()

# --- FastAPI приложение ---
app = FastAPI(lifespan=lifespan)

@app.post(WEBHOOK_PATH)
async def webhook(request: Request) -> Response:
    """Telegram будет слать обновления сюда"""
    update = types.Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    return Response(status_code=200)

@app.get("/health")
async def health():
    return {"status": "ok"}