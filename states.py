from aiogram.fsm.state import State, StatesGroup

class OrderForm(StatesGroup):
    service = State()
    master = State()
    name = State()
    phone = State()
    time = State()