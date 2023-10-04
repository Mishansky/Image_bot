from aiogram import types, bot
from loader import dp
from States.input_photo import PhotoState
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


import os

@dp.callback_query_handler(lambda query: query.data == "upload_photo")
async def start_uploading_photo(call: types.CallbackQuery):
    await PhotoState.waiting_for_photo.set()
    await call.message.answer("Отправте картинку которую хотите отправить")


@dp.message_handler(content_types=types.ContentType.PHOTO, state=PhotoState.waiting_for_photo)
async def get_photo(message:types.Message,state: FSMContext):

    file_path = r"C:\Users\misha\PycharmProjects\MyFirstTGbot\handlers\img"
    file_path = rf"{file_path}\{len(os.listdir(file_path))+1}.jpg"

    await message.photo[-1].download(file_path)

    await state.finish()
    await message.answer("фотография принята!")




