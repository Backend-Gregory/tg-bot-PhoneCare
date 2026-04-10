# Телеграм-бот для мастерской по ремонту телефонов

Бот-визитка с записью на услуги.

## Функционал

- 📞 Контакты
- 💼 Услуги
- 💰 Цены
- 📍 Адрес
- ❓ Помощь
- 📝 Записаться (опрос: имя → телефон)

## Команды

- `/start` — главное меню
- `/cancel` — отмена записи

## Технологии

- Python 3.10
- aiogram 3.x
- FSM (машина состояний)

## Ссылка на бота

👉 [@phonecare_bot](https://t.me/phonecare_bot)

## Установка и запуск (локально)

```bash
git clone https://github.com/Backend-Gregory/tg-bot-PhoneCare.git
cd tg-bot-PhoneCare
pip install -r requirements.txt
python main.py