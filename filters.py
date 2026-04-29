from aiogram.filters import BaseFilter
from aiogram.types import Message
from config import ADMIN_ID

class IsAdmin(BaseFilter):
    def __call__(self, message: Message):
        return message.from_user.id == ADMIN_ID