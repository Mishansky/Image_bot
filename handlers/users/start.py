from aiogram import types,bot
from loader import dp
from keyboards.inline_keyboards.keyboard_from_work import inline_kb_first_menu
from aiogram.dispatcher import FSMContext
from States.input_photo import PhotoState

@dp.message_handler(text = "/start")
async def command_start(message:types.Message):
    await message.answer(f"Привет  {message.from_user.full_name}!  \n"
                         f"Что будем делать?",reply_markup=inline_kb_first_menu)











