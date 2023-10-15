from loader import dp
from aiogram import types
from loader import bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from PIL import Image, ImageDraw, ImageFont
import requests
import io
import os

@dp.callback_query_handler(lambda query: query.data == "button2")
async def view_photos(message: types.Message,call = True):
    im = "images"

    if not os.path.exists(im):
        await message.answer("Нет сохраненных фотографий.")
        return

    # Получить список файлов в папке
    files = [f for f in os.listdir(im) if os.path.isfile(os.path.join(im, f))]

    if not files:
        await message.answer("Нет сохраненных фотографий.")
        return

    # Отправить первую фотографию с кнопками "назад" и "вперед"
    await send_photo_with_buttons(message.from_user.id, im, files, 0, None)


async def send_photo_with_buttons(chat_id, im, files, index, prev_message_id=None):


    with open(os.path.join(im, files[index]), 'rb') as photo_file:
        markup = InlineKeyboardMarkup()
        if index > 0:
            prev_button = InlineKeyboardButton("Назад", callback_data=f"prev_{index}")
            markup.add(prev_button)
        if index < len(files) - 1:
            next_button = InlineKeyboardButton("Вперед", callback_data=f"next_{index}")
            markup.add(next_button)

        # Добавляем кнопку "Выбрать" для редактирования фотографии
        select_button = InlineKeyboardButton("Выбрать", callback_data=f"select_{index}")
        markup.add(select_button)

        caption = f"Фото {index + 1} из {len(files)}"

        if prev_message_id:
            try:
                # Попробуйте удалить предыдущее сообщение с фотографией
                await bot.delete_message(chat_id, prev_message_id)
            except Exception as e:
                # Обработка ошибки, если сообщение уже удалено или не существует
                pass

        message = await bot.send_photo(chat_id, photo=photo_file, caption=caption, reply_markup=markup)

        return message.message_id

@dp.callback_query_handler(lambda c: c.data and c.data.startswith(('prev_', 'next_', 'select_')))
async def handle_callback_query(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data.startswith('prev_'):
        index = int(callback_query.data.split('_')[1]) - 1
    elif callback_query.data.startswith('next_'):
        index = int(callback_query.data.split('_')[1]) + 1
    else:
        index = int(callback_query.data.split('_')[1])

    im = "images"

    if not os.path.exists(im):
        await callback_query.answer("Нет сохраненных фотографий.")
        return

    # Получить список файлов в папке
    files = [f for f in os.listdir(im) if os.path.isfile(os.path.join(im, f))]

    if not files:
        await callback_query.answer("Нет сохраненных фотографий.")
        return



    if callback_query.data.startswith('select_'):
        # Если нажата кнопка "Выбрать", сохраняем индекс в состояние пользователя
        async with state.proxy() as data:
            data['photo_index'] = index
        # Отправляем запрос на ввод текста
        await bot.send_message(callback_query.from_user.id, "Пожалуйста, введите текст, который вы хотите добавить на фотографию:")
        return

    if 0 <= index < len(files):
        prev_message_id = callback_query.message.message_id if callback_query.message else None
        message_id = await send_photo_with_buttons(callback_query.from_user.id, im, files, index, prev_message_id)
        try:
            # Попробуйте удалить предыдущее сообщение с фотографией
            await bot.delete_message(callback_query.from_user.id, prev_message_id)
        except Exception as e:
            # Обработка ошибки, если сообщение уже удалено или не существует
            pass

    await callback_query.answer()
@dp.message_handler(lambda message: message.text)
async def handle_text_input(message: types.Message, state: FSMContext):
    text = message.text

    async with state.proxy() as data:
        index = data.get("photo_index")

    im = "images"

    if not os.path.exists(im):
        await message.reply("Нет сохраненных фотографий.")
        return

    files = [f for f in os.listdir(im) if os.path.isfile(os.path.join(im, f))]

    if not (0 <= index < len(files)):
        await message.reply("Неверный индекс фотографии.")
        return

    # Открываем выбранную фотографию с помощью Pillow
    with Image.open(os.path.join(im, files[index])) as img:
        # Добавляем текст на фотографию
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", size=40)
        text_width, text_height = draw.textsize(text, font=font)
        x = (img.width - text_width) / 100
        y = img.height - text_height - 100
        draw.text((x, y), text, fill="white", font=font)


        if not os.path.exists("EDIT_PHOTO"):
            os.mkdir("EDIT_PHOTO")
        # Сохраняем отредактированную фотографию
        edited_photo_path = os.path.join("EDIT_PHOTO", f"edited_{index}.png")
        img.save(edited_photo_path)

        # Отправляем отредактированную фотографию пользователю
        with open(edited_photo_path, 'rb') as edited_photo_file:
            await message.reply_photo(photo=edited_photo_file)

        # Очищаем состояние пользователя
        await state.finish()


