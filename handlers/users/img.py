from aiogram import types, bot
from loader import dp
from States.input_photo import PhotoState
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards.inline_keyboards.exit_kb import exit_kb_menu
from keyboards.inline_keyboards.all_buttons import AllButtons
import requests
from PIL import Image, ImageFilter

import os
import io
from data.config import BOT_TOKEN





@dp.callback_query_handler(lambda query: query.data == "upload_photo")
async def start_uploading_photo(call: types.CallbackQuery):
    await call.message.delete()
    await PhotoState.waiting_for_photo.set()
    await call.message.answer("Отправьте картинку которую хотите отправить", reply_markup=exit_kb_menu)



URI_INFO = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id="


@dp.message_handler(content_types=["photo"], state=PhotoState.waiting_for_photo)
async def get_photo(message: types.Message, state: FSMContext):
    URI = f"https://api.telegram.org/file/bot{BOT_TOKEN}/"

    file_id = message.photo[2].file_id
    resp = requests.get(URI_INFO + file_id)
    img_path = resp.json()["result"]["file_path"]
    img = requests.get(URI + img_path)
    img = Image.open(io.BytesIO(img.content))

    im = "images"
    if not os.path.exists("images"):
        os.mkdir("images")

    # Получить список файлов в папке
    files = [f for f in os.listdir(im) if os.path.isfile(os.path.join(im, f))]

    # Если количество файлов превышает 10, удалить первый файл и сдвинуть остальные
    if len(files) >= 10:
        os.remove(os.path.join(im, files[0]))
        for i in range(1, len(files)):
            os.rename(os.path.join(im, files[i]), os.path.join(im, f"{i - 1}.png"))

    # Сохранить новую фотографию
    new_filename = f"images/{len(files) - 1}.png"
    img.save(new_filename, format="PNG")

    await state.finish()
    await message.answer("Фотография принята! Жду следующей!", reply_markup=AllButtons)