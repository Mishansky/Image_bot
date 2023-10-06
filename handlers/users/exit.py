from aiogram import types, bot
from loader import dp
from aiogram.dispatcher import FSMContext
from States.input_photo import PhotoState

from keyboards.inline_keyboards.keyboard_from_work import inline_kb_first_menu

@dp.callback_query_handler(lambda query: query.data == 'exit',state=PhotoState.waiting_for_photo)
async def command_exit(call: types.CallbackQuery, state: FSMContext):

    await call.message.answer(f"Привет    \n"
                         f"Что будем делать?", reply_markup=inline_kb_first_menu)


