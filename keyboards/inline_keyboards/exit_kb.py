from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

exit_kb = InlineKeyboardButton("Назад", callback_data="exit")

exit_kb_menu = InlineKeyboardMarkup().add(exit_kb)