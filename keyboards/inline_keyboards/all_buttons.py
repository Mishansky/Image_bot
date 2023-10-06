from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

exit_kb = InlineKeyboardButton("Назад", callback_data="exit")

inl_work_btn = InlineKeyboardButton("Создаем шаблон", callback_data="upload_photo")
inl_work_btn2 = InlineKeyboardButton("Создаем картинку", callback_data="button2")

AllButtons = InlineKeyboardMarkup().add(inl_work_btn).add(inl_work_btn2).add(exit_kb)




