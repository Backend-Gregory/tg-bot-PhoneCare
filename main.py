import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
import os

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class OrderForm(StatesGroup):
    name = State
    phone = State

kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='📞 Контакты'), KeyboardButton(text='💼 Услуги')],
        [KeyboardButton(text='💰 Цены'), KeyboardButton(text='📍 Адрес')],
        [KeyboardButton(text='❓ Помощь')],
        [KeyboardButton(text='📝 Записаться')]
    ],
    resize_keyboard=True
)

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
    if not message.text.strip():
        await message.answer('Введите текст')
        return
    if len(message.text) > 100:
        await message.answer("❌ Слишком длинное имя. Используй не больше 100 символов.")
        return
    await state.update_data(name=message.text)
    await state.set_state(OrderForm.phone)
    await message.answer('Какой номер телефона?')

@dp.message(OrderForm.phone)
async def get_phone(message: types.Message, state: FSMContext):
    if not message.text.strip():
        await message.answer('Введите текст')
        return
    if len(message.text) > 100:
        await message.answer("❌ Слишком длинный телефон. Используй не больше 100 символов.")
        return
    await state.update_data(phone=message.text)
    data = await state.get_data()
    name = data.get('name')
    phone = data.get('phone')

    try:
        await bot.send_message(ADMIN_ID, f"📝 Новая заявка!\nИмя: {name}\nТелефон: {phone}")
        await message.answer('✅ Спасибо! Мы свяжемся с вами.', reply_markup=kb)

        await state.clear()
    except Exception:
        await message.answer("❌ Техническая ошибка. Попробуйте позже.")

@dp.message(Command('cancel'))
async def cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('Опрос отменен', reply_markup=kb)

@dp.message()
async def handle_menu(message: types.Message):
    if message.text == '📞 Контакты':
        await message.answer(
            'Телефон: +7 (999) 123-45-67\n'
            'Telegram: @phonecare\n'
            'Время работы: 10:00–20:00'
        )
    
    elif message.text == '💼 Услуги':
        await message.answer(
            '• Замена экрана\n'
            '• Замена аккумулятора\n'
            '• Диагностика\n'
            '• Ремонт кнопок'
        )

    elif message.text == '💰 Цены':
        await message.answer(
            '• Замена экрана — от 2000₽\n'
            '• Аккумулятор — от 1500₽\n'
            '• Диагностика — 500₽ (бесплатно при ремонте)'
        )
    
    elif message.text == '📍 Адрес':
        await message.answer(
            '📍 г. Москва, ул. Строителей, д. 15\n'
            '🚇 м. Фрунзенская, выход к рынку'
        )
    
    elif message.text == '❓ Помощь':
        await message.answer(
            '📌 Используй кнопки меню.\n'
            'По вопросам пиши @phonecare'
        )
    
    else:
        await message.answer('Используй кнопки.', reply_markup=kb)

async def main():
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())