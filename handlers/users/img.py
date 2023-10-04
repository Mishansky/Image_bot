from aiogram import types, bot
from loader import dp
from States.input_photo import action_photo

import os

@dp.message_handler(content_types=types.ContentType.PHOTO, state=action_photo.inp_photo)
async def get_photo(message:  types.Message):

    await message.answer("Отправь фотографию которую нужно сделать шаблоном!")
    file_path = r"C:\Users\misha\PycharmProjects\MyFirstTGbot\handlers\img"
    file_path = rf"{file_path}\{len(os.listdir(file_path))+1}.jpg"

    await message.photo[-1].download(file_path)





