from aiogram import types, bot
from loader import dp
from States.input_photo import PhotoState
from aiogram.dispatcher import FSMContext
from keyboards.inline_keyboards.exit_kb import exit_kb_menu
from keyboards.inline_keyboards.all_buttons import AllButtons


import os

@dp.callback_query_handler(lambda query: query.data == "upload_photo")
async def start_uploading_photo(call: types.CallbackQuery):
    await call.message.delete()
    await PhotoState.waiting_for_photo.set()
    await call.message.answer("Отправьте картинку которую хотите отправить", reply_markup=exit_kb_menu)





@dp.message_handler(content_types=types.ContentType.PHOTO, state=PhotoState.waiting_for_photo)
async def get_photo(message:types.Message,state: FSMContext):
    await message.delete()

    file_path = r"C:\Users\misha\PycharmProjects\MyFirstTGbot\handlers\img"
    file_path = rf"{file_path}\{len(os.listdir(file_path))+1}.jpg"

    await message.photo[-1].download(file_path)


    await message.answer("фотография принята!, Жду следующей!", reply_markup=AllButtons)




