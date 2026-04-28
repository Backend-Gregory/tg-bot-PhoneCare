from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

service_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Замена экрана'), KeyboardButton(text='Замена аккумулятора')],
        [KeyboardButton(text='Диагностика'), KeyboardButton(text='Ремонт кнопок')]
    ],
    resize_keyboard=True
)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='📞 Контакты'), KeyboardButton(text='💼 Услуги')],
        [KeyboardButton(text='💰 Цены'), KeyboardButton(text='📍 Адрес')],
        [KeyboardButton(text='❓ Помощь')],
        [KeyboardButton(text='📝 Записаться')]
    ],
    resize_keyboard=True
)