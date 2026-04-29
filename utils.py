import re
from html import escape

def format_order_message(data: dict) -> str:
    return (
        f"📝 Новая заявка!\n\n"
        f"Услуга: {escape(data.get('service', '?'))}\n"
        f"Мастер: {escape(data.get('master', '?'))}\n"
        f"Имя: {escape(data.get('name', '?'))}\n"
        f"Телефон: {escape(data.get('phone', '?'))}\n"
        f"Время: {escape(data.get('time', '?'))}"
    )

def validate_phone(phone: str) -> bool:
    clean_phone = re.sub(r'[\s\-\(\)]', '', phone)
    pattern = r'^(\+7|8)\d{10}$'
    return bool(re.match(pattern, clean_phone))