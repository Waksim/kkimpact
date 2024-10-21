import io
import os
import re
import sqlite3
import time
from io import BytesIO
from typing import List

from aiogram.types import BufferedInputFile, InputFile, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, \
    WebAppInfo
from aiogram_media_group import media_group_handler
from loguru import logger

from aiogram.enums import ParseMode, ContentType
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram import types, Router, Bot, html, F
from aiogram.filters.command import Command

from filters.chat_type import ChatTypeFilter
from functions import generate_deck
from functions.card_recognition import recognize_deck_img
from functions.create_image import create_decks_img
from functions.decryption_of_the_code import decrypt_code, card_codes_to_deck_code, get_card_name_by_card_code
from functions.get_role_card_names import get_role_card_names
from config import settings


bot = Bot(token=settings.bot_token)

others = Router()

others.message.filter(
    ChatTypeFilter(chat_type=["private"])
)


# @others.message(F.sticker)
# async def cmd_start(message: types.Message):
#     sticker_uid = message.sticker.file_unique_id
#     # print(message.sticker)
#     sqlite_connection = sqlite3.connect('tcgCodes.sqlite')
#     cursor = sqlite_connection.cursor()
#
#     cursor.execute("SELECT id, card_name_ru FROM main.role_cards WHERE sticker_uid = '0' ")
#     r = cursor.fetchall()
#     # print(r)
#     current_card = r[0]
#     if len(r) == 1:
#         next_card = ['-', '-']
#     else:
#         next_card = r[1]
#
#     cursor.execute("UPDATE main.role_cards SET sticker_uid = ? WHERE id = ?;", (sticker_uid, current_card[0]))
#     sqlite_connection.commit()
#     cursor.close()
#
#     await message.answer(f"UID стикера: {sticker_uid}\n"
#                          f"Добавлен стикер: {current_card[1]}, id: {current_card[0]}\n"
#                          f"Следующая карта: {next_card[1]}, id: {next_card[0]}")
#
#
# # ____________________________________________________________________




@others.message(F.media_group_id, F.content_type.in_({'photo'}))
@media_group_handler
async def album_handler(messages: List[types.Message]):
    await bot.send_chat_action(chat_id=messages[-1].from_user.id, action="upload_photo")
    start_time = time.time()
    logger.info(f"@{messages[-1].from_user.username} – 'ФОТО-АЛЬБОМ'")

    album_builder = MediaGroupBuilder()
    caption_text = ''
    c = 1
    file_path_arr = []
    deck_code_arr = []
    print(f"{len(messages)} фото получено")
    for m in messages:
        file_id = m.photo[-1].file_id
        print(file_id)

        file = await bot.get_file(file_id)
        file_path = file.file_path

        current_time = int(time.time())
        user_id = messages[-1].from_user.id
        # if user_id == 382202500:
        if user_id == 440055388:
            user_id = "moria"

        image_name = f'{str(user_id)}_{str(current_time)}.jpg'

        await bot.download_file(file_path=file_path, destination=f'./img/assets/decks_img/{image_name}')
        file_path_arr.append(f'./img/assets/decks_img/{image_name}')

        try:
            debug_photo_path, role_card_codes, action_card_codes = recognize_deck_img(image_name, debug_mode=0)

            deck_code = card_codes_to_deck_code(role_card_codes, action_card_codes)
            deck_code_arr.append(deck_code)

            card_names_str = get_card_name_by_card_code(role_card_codes)
            caption_text += f"{c}. {html.bold(html.quote(card_names_str))}\n" + html.code(html.quote(deck_code)) + "\n\n"
            c += 1

            # debug_photo = FSInputFile(debug_photo_path)
            photo = create_decks_img(role_cards=role_card_codes, action_cards=action_card_codes)
            album_builder.add_photo(media=photo, parse_mode=ParseMode.HTML)
        except:
            continue

        # album_builder.add_photo(media=debug_photo, parse_mode=ParseMode.HTML)

    # await messages[-1].answer_media_group(media=album_builder.build())

    caption_text += "\n--- %s seconds ---" % (round(time.time() - start_time, 2))

    if len(caption_text) < 1000:
        album_builder.caption = caption_text
        await messages[-1].reply_media_group(media=album_builder.build())
    else:
        await messages[-1].reply_media_group(media=album_builder.build())
        await messages[-1].answer(caption_text, parse_mode=ParseMode.HTML)

    for file_path in file_path_arr:
        try:
            os.remove(file_path)
        except FileNotFoundError:
            continue

    logger.info("\n".join(deck_code_arr))

    print("--- %s seconds ---" % (round(time.time() - start_time, 2)))

    messages_id = [m.message_id for m in messages]

    await bot.delete_messages(messages[-1].from_user.id, messages_id)


@others.message(F.photo)
async def photo_recognition(message: types.Message):
    await bot.send_chat_action(chat_id=message.from_user.id, action="upload_photo")
    logger.info(f"@{message.from_user.username} – 'ФОТО'")

    file = await bot.get_file(message.photo[-1].file_id)
    file_path = file.file_path

    current_time = int(time.time())
    user_id = message.from_user.id
    if user_id == 382202500:
        # if user_id == 440055388:
        user_id = "moria"

    image_name = f'{str(user_id)}_{str(current_time)}.jpg'

    await bot.download_file(file_path=file_path, destination=f'./img/assets/decks_img/{image_name}')

    album_builder = MediaGroupBuilder()

    debug_photo_path, role_card_codes, action_card_codes = recognize_deck_img(image_name)

    deck_code = card_codes_to_deck_code(role_card_codes, action_card_codes)

    card_names_str = get_card_name_by_card_code(role_card_codes)
    caption_text = f"{html.bold(html.quote(card_names_str))}\n" + html.code(html.quote(deck_code)) + "\n"
    album_builder.caption = caption_text

    debug_photo = FSInputFile(debug_photo_path)
    photo = create_decks_img(role_cards=role_card_codes, action_cards=action_card_codes)
    album_builder.add_photo(media=photo, parse_mode=ParseMode.HTML)

    album_builder.add_photo(media=debug_photo, parse_mode=ParseMode.HTML)

    await message.answer_media_group(media=album_builder.build())

    try:
        os.remove(debug_photo_path)
    except FileNotFoundError:
        pass

    try:
        os.remove(f'./img/assets/decks_img/{image_name}')
    except FileNotFoundError:
        pass

    logger.info(deck_code)


    # role_cards, action_cards = recognize_deck_img(photo)
    # await message.answer(str(role_cards, action_cards), parse_mode=ParseMode.HTML)


@others.message(Command("kk", "Kk", "kK", "KK", "кк", "Кк", "кК", "КК"))
async def decoding_code(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    max_length = 4000

    arg = message.text.split(" ")
    print(arg)
    print(len(arg))
    if len(arg) == 1:
        arg = message.text.split("\n")

    if len(arg) >= 2:
        arg1 = arg[1].lower()

        if arg1 == 'td' or arg1 == 'пд' or arg1 == 'наказание' or arg1 == 'правда действие' or arg1 == 'правда или действие' or arg1 == 'тд':

            # Подключаемся к базе данных
            conn = sqlite3.connect('tcgCodes.sqlite')  # Укажите путь к вашей базе данных
            cursor = conn.cursor()

            if len(arg) == 2:
                arg2 = "1"
                arg.append(arg2)

            if len(arg) == 3:
                arg2 = int(arg[2].lower())
                print(arg2)

                try:
                    limit = int(arg2)  # Преобразуем аргумент в целое число
                except ValueError:
                    print("Ошибка: аргумент должен быть целым числом.")
                    await message.answer("Пожалуйста, введите корректное число.")
                    return

                # Выполняем SQL-запрос для получения случайных строк
                cursor.execute(f"SELECT * FROM td ORDER BY RANDOM() LIMIT {limit}")
                rows = cursor.fetchall()

                if limit == 0:
                    limit = 4

                    # Запрос для получения всех значений из столбца 'text'
                    cursor.execute(f"SELECT * FROM td ORDER BY RANDOM() LIMIT {limit}")
                    rows = cursor.fetchall()

                    # Проверяем, что в таблице достаточно данных
                    if len(rows) < limit:
                        print("Недостаточно данных в таблице.")
                    else:
                        # Выбираем 4 случайных значения
                        qw = []
                        for row in rows:
                            qw.append(row[1])

                        caption_text = (
                                    f"{html.bold('для НЕГО: ')}\n - {qw[0]}\n - {qw[1]}\n" + f"{html.bold('для НЕЕ: ')}\n - {qw[2]}\n - {qw[3]}")

                        if len(caption_text) > max_length:
                            caption_text = caption_text[:max_length]  # Обрезаем строку до 4000 символов

                        # Отправляем сообщение с вопросами
                        await message.answer(caption_text, parse_mode=ParseMode.HTML)
                    return
                else:
                    # Проверяем, что в таблице достаточно данных
                    if len(rows) < limit:
                        print("Недостаточно данных в таблице.")
                        await message.answer("Недостаточно данных в таблице.")

                    # Формируем строку с вопросами
                    questions = ""
                    for counter, row in enumerate(rows, start=1):  # Используем enumerate для подсчета
                        questions += f"{counter}. {row[1]}\n"  # Предполагается, что текст вопроса находится в первом столбце

                    caption_text = f"{html.bold('Вопросы правда или действие: ')}\n{questions}"

                    # Отправляем сообщение с вопросами
                    if len(caption_text) > max_length:
                        caption_text = caption_text[:max_length]  # Обрезаем строку до 4000 символов

                    # Отправляем сообщение с вопросами
                    await message.answer(caption_text, parse_mode=ParseMode.HTML)
                    return


# ____________________________________________________________________
@others.message(Command("generate_text_10"))
async def generate_text_10(message: types.Message):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    caption_text = ''
    counter = 10

    for i in range(1, counter + 1):
        generated_deck = generate_deck.get_random_code(card_name_lang='card_name_ru')
        deck_code = generated_deck[0]
        deck_role_cards = generated_deck[1]

        caption_text += (f"{i}) {html.bold(html.quote(deck_role_cards))}\n" +
                         html.code(html.quote(deck_code)) + "\n")

    await message.answer(caption_text, parse_mode=ParseMode.HTML)


@others.message()
async def deck_code_decoder(message: types.Message):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    if message.from_user.id not in [382202500, 799890260]:
        logger.info(f"@{message.from_user.username} – '{message.text}'")

    sqlite_connection = sqlite3.connect('./users_info.sqlite')
    cursor = sqlite_connection.cursor()
    tg_id = message.from_user.id
    cursor.execute("SELECT preferens FROM telegram_users where tg_id = ?;", (tg_id,))
    preference = cursor.fetchall()[0][0]

    result = re.findall(r'([^.,\'\"\s\n\t\r]{68})', message.text)

    if len(result) == 1:
        deck_code = result[0]
        decrypted_data = decrypt_code(deck_code)

        if len(decrypted_data[0]) == 0 and len(decrypted_data[1]) == 0:
            await message.reply_sticker('CAACAgIAAxkBAAEMdzxmjoaHzm6a5GZ1N6C5ZKbPtOeoCAAC9FgAAgmGeEhYrQGzIHlCKzUE')
            return

        role_cards = decrypted_data[0]
        action_cards = decrypted_data[1]

        photo = create_decks_img(role_cards=role_cards, action_cards=action_cards)

        names_line = get_role_card_names(role_cards=role_cards, lang=preference)

        answer_text = (f"{html.bold(html.quote(names_line))}\n" +
                       html.code(html.quote(deck_code)))

        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=answer_text, parse_mode=ParseMode.HTML)

    if len(result) > 1:
        album_builder = MediaGroupBuilder()
        caption_text = ''
        c = 1
        for deck_code in result:
            decrypted_data = decrypt_code(deck_code)

            if len(decrypted_data[0]) == 0 and len(decrypted_data[1]) == 0:
                continue

            role_cards = decrypted_data[0]
            action_cards = decrypted_data[1]

            photo = create_decks_img(role_cards=role_cards, action_cards=action_cards)

            names_line = get_role_card_names(role_cards=role_cards, lang=preference)
            answer_text = f"{html.bold(html.quote(names_line))}\n" + html.code(html.quote(deck_code))
            caption_text += str(c) + ') ' + answer_text + '\n'

            album_builder.add_photo(media=photo, parse_mode=ParseMode.HTML)

            if c == 10:
                break
            c += 1

        if c == 1:
            await message.reply_sticker('CAACAgIAAxkBAAEMdzxmjoaHzm6a5GZ1N6C5ZKbPtOeoCAAC9FgAAgmGeEhYrQGzIHlCKzUE')
        elif len(caption_text) < 1000:
            album_builder.caption = caption_text
            await message.reply_media_group(media=album_builder.build())
        else:
            await message.reply_media_group(media=album_builder.build())
            await message.answer(caption_text, parse_mode=ParseMode.HTML)

    if len(result) == 0:

        if preference == 'ru':
            await message.answer_sticker('CAACAgIAAxkBAAELtW1l9F1HaBegi38I5sgl4ZI4iJVRywACuEEAAiJ7oEum7CjZwpzpFTQE')

        elif preference == 'eng':
            await message.answer_sticker('CAACAgIAAxkBAAELtW9l9F7l2UB9chap87fDirNaadr2CAACMEgAAq9SoEvlrLUFQwbKhzQE')

        elif preference == 'ua':
            await message.answer_sticker('CAACAgIAAxkBAAELtXFl9F7pWWZ9ZuW4fTbIh8KBIW5jYwACSkYAAilOoEvU9QcnB8gr5DQE')

        elif preference == 'cn':
            await message.answer_sticker('CAACAgIAAxkBAAELtXNl9F7sgBFn55fH4tdW8spKRFQa6QACpksAAsnzqEtU_IL8WHoHBTQE')

        await message.answer(
            'Commands:\n/start\n/choose_lang',
            parse_mode=ParseMode.HTML
        )


# ____________________________________________________________________

# @others.message(Command('delete_sticker_pack'))
# async def cmd_start(message: types.Message):
#     sticker_name = 'dendro_by_KKImpact_testBOT'
#     result: bool = await bot.delete_sticker_set(sticker_name)
#     await message.answer(f"Удален стикерпак: https://t.me/addstickers/{sticker_name}")
#
#
# @others.message(Command('create_sticker_pack'))
# async def cmd_start(message: types.Message):
#     # await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
#     # sticker_id = message.sticker.file_id
#     sticker_name = 'geo_by_KKImpact_testBOT'
#     # sticker_pack_info = ''
#
#     # time.sleep(10)
#     stickers_arr = []
#
#     sqlite_connection = sqlite3.connect('tcgCodes.sqlite')
#     cursor = sqlite_connection.cursor()
#
#     cursor.execute("SELECT code, element FROM main.role_cards")
#     codes = cursor.fetchall()
#
#     counter = 0
#
#     for code in codes:
#         if counter == 49:
#             print(counter)
#             break
#         element = code[1].split(', ')[0]
#         if element == 'geo':
#             stickers_arr.append(types.InputSticker(sticker=types.FSInputFile(f'img/role_cards_stickers/{code[0]}.png'),
#                                                    emoji_list=['🟢']))
#             counter += 1
#
#     result: bool = await bot.create_new_sticker_set(user_id=message.from_user.id,
#                                                     name=sticker_name,
#                                                     title='🌕 GEO 🌕 @KKimpactBOT',
#                                                     stickers=stickers_arr,
#                                                     sticker_format='static',
#                                                     sticker_type='regular'
#                                                     )
#
#     await message.answer(f"Создан стикерпак: https://t.me/addstickers/{sticker_name}")



