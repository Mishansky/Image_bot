from aiogram.dispatcher.filters.state import StatesGroup,State

class PhotoState(StatesGroup):
    waiting_for_photo = State()

