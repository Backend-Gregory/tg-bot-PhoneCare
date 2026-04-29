from collections import defaultdict
from datetime import datetime
from aiogram import BaseMiddleware
from aiogram.types import Message

class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, interval: int = 1) -> None:
        super().__init__()
        self.interval = interval
        self.user_last_message = {}
    
    async def __call__(self, handler, event: Message, data):
        if not isinstance(event, Message):
            return await handler(event, data)
        user_id = event.from_user.id
        now = datetime.now()
        last = self.user_last_message.get(user_id, datetime.min)

        if (now - last).seconds < self.interval:
            await event.answer("⏳ Подождите секунду")
            return
        
        self.user_last_message[user_id] = now
        return await handler(event, data)