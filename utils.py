def format_order_message(data: dict) -> str:
    return (
        f"📝 Новая заявка!\n\n"
        f"Услуга: {data.get('service')}\n"
        f"Мастер: {data.get('master')}\n"
        f"Имя: {data.get('name')}\n"
        f"Телефон: {data.get('phone')}\n"
        f"Время: {data.get('time')}"
    )