from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inl_work_btn = InlineKeyboardButton("Создаем шаблон", callback_data="button1")
inl_work_btn2 = InlineKeyboardButton("Создаем картинку", callback_data="button2")

inline_kb_first_menu = InlineKeyboardMarkup().add(inl_work_btn).add(inl_work_btn2)



