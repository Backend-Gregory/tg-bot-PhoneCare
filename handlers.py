import logging
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

from config import ADMIN_ID, MAX_NAME_LENGTH, MAX_PHONE_LENGTH, MAX_TIME_LENGTH, MASTERS
from database import session, Order
from keyboards import service_kb, main_kb
from states import OrderForm
from utils import format_order_message

router = Router()

@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Привет! Я бот мастерской PhoneCare.\n"
        "Отремонтируем твой телефон быстро и недорого.\n"
        "Выбери нужный раздел на кнопках ниже 👇",
        reply_markup=main_kb
    )

@router.message(lambda message: message.text == '📝 Записаться')
async def start_order(message: types.Message, state: FSMContext):
    await state.set_state(OrderForm.service)
    await message.answer('Выбор услуги:', reply_markup=service_kb)

@router.message(OrderForm.service)
async def get_service(message: types.Message, state: FSMContext):
    if message.text not in MASTERS:
        await message.answer('Используй кнопки', reply_markup=service_kb)
        return
    await state.update_data(service=message.text)
    await state.set_state(OrderForm.master)
    master_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=master)] for master in MASTERS[message.text]
        ],
        resize_keyboard=True
    )
    await state.update_data(master_kb=master_kb)
    await message.answer("Выбери мастера:", reply_markup=master_kb)

@router.message(OrderForm.master)
async def get_master(message: types.Message, state: FSMContext):
    data = await state.get_data()
    service = data.get("service")
    master_kb = data.get("master_kb")
    if message.text not in MASTERS.get(service, []):
        await message.answer("❌ Выбери мастера из списка", reply_markup=master_kb)
        return
    
    await state.update_data(master=message.text)
    await state.set_state(OrderForm.name)
    await message.answer('Как тебя зовут?', reply_markup=ReplyKeyboardRemove())

@router.message(OrderForm.name)
async def get_name(message: types.Message, state: FSMContext):
    if not message.text or not message.text.strip():
        await message.answer('❌ Введите текст')
        return
    if len(message.text) > MAX_NAME_LENGTH:
        await message.answer(f"❌ Слишком длинное имя (макс {MAX_NAME_LENGTH} символов)")
        return
    await state.update_data(name=message.text)
    await state.set_state(OrderForm.phone)
    await message.answer('Какой у вас номер телефона?')
    
@router.message(OrderForm.phone)
async def get_phone(message: types.Message, state: FSMContext):
    if not message.text or not message.text.strip():
        await message.answer('Введите текст')
        return
    if len(message.text) > MAX_PHONE_LENGTH:
        await message.answer(f"❌ Слишком длинный телефон (макс {MAX_PHONE_LENGTH} символов)")
        return
    await state.update_data(phone=message.text)
    await state.set_state(OrderForm.time)
    await message.answer("Напиши удобное время и дату (например: завтра в 15:00)")

@router.message(OrderForm.time)
async def get_time(message: types.Message, state: FSMContext):
    if not message.text.strip():
        await message.answer('❌ Введите текст')
        return
    if len(message.text) > MAX_TIME_LENGTH:
        await message.answer(f'❌ Слишком длинное время (макс {MAX_TIME_LENGTH} символов)')
        return
    await state.update_data(time=message.text)
    data = await state.get_data()

    service = data.get('service')
    master = data.get('master')
    name = data.get('name')
    phone = data.get('phone')
    time = data.get('time')

    order = Order(
        service=service,
        master=master,
        name=name,
        phone=phone,
        time=time
    )

    try:
        session.add(order)
        session.commit()
        print('Заявка сохранена в БД')

        text = format_order_message(data)
        await message.bot.send_message(ADMIN_ID, text)
        await message.answer('✅ Спасибо! Мы свяжемся с вами.', reply_markup=main_kb)
        await state.clear()
    except Exception as e:
        session.rollback()
        await state.clear()
        logging.error(f"Ошибка отправки админу: {e}")
        await message.answer("❌ Техническая ошибка. Попробуйте позже.", reply_markup=main_kb)

@router.message(Command('cancel'))
async def cancel(message: types.Message, state: FSMContext):
    if await state.get_state() is None:
        await message.answer("Нет активного опроса")
        return
    await state.clear()
    await message.answer('Опрос отменён', reply_markup=main_kb)

@router.message()
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
        await message.answer('Используй кнопки.', reply_markup=main_kb)