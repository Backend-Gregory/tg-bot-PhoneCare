import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Константы
MAX_NAME_LENGTH = 100
MAX_PHONE_LENGTH = 100
MAX_TIME_LENGTH = 200
MASTERS = {
    "Замена экрана": ["Антон", "Дмитрий"],
    "Замена аккумулятора": ["Антон", "Сергей"],
    "Диагностика": ["Сергей"],
    "Ремонт кнопок": ["Антон", "Дмитрий"]
}