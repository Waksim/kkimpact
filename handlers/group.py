import os
import re
import sqlite3
import time
from datetime import datetime
from typing import List

from aiogram.exceptions import TelegramBadRequest
from aiogram_media_group import media_group_handler
from loguru import logger

from aiogram import Router, Bot, html, F, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from filters.chat_type import ChatTypeFilter
from functions import generate_deck, random_hoyolab
from functions.card_recognition import recognize_deck_img
from functions.create_image import create_decks_img
from functions.decryption_of_the_code import decrypt_code, card_codes_to_deck_code, get_card_name_by_card_code
from functions.get_role_card_names import get_role_card_names
from config import settings


bot = Bot(token=settings.bot_token)

group = Router()
group.message.filter(
    ChatTypeFilter(chat_type=["group", "supergroup"])
)


@group.message(F.media_group_id, F.content_type.in_({'photo'}))
@media_group_handler
async def album_handler(messages: List[types.Message]):
    # print(messages[0].caption)
    caption = [m.caption for m in messages if m.caption is not None][0]
    # print(caption)
    if caption not in ["/kk", "/Kk", "/kK", "/KK", "/кк", "/Кк", "/кК", "/КК"]:
        print('skip')
        return

    await bot.send_chat_action(chat_id=messages[-1].chat.id, action="upload_photo")
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
        except:
            continue

        # debug_photo = FSInputFile(debug_photo_path)
        photo = create_decks_img(role_cards=role_card_codes, action_cards=action_card_codes)
        album_builder.add_photo(media=photo, parse_mode=ParseMode.HTML)

        # album_builder.add_photo(media=debug_photo, parse_mode=ParseMode.HTML)

    # await messages[-1].answer_media_group(media=album_builder.build())

    caption_text += "\n--- %s seconds ---" % (round(time.time() - start_time, 2))

    if len(caption_text) < 1000:
        album_builder.caption = caption_text
        await messages[-1].reply_media_group(media=album_builder.build())
    else:
        await messages[-1].reply_media_group(media=album_builder.build())
        await messages[-1].answer(caption_text, parse_mode=ParseMode.HTML)

    # os.remove(debug_photo_path)
    for file_path in file_path_arr:
        try:
            os.remove(file_path)
        except FileNotFoundError:
            continue

    logger.info("\n".join(deck_code_arr))

    print("--- %s seconds ---" % (round(time.time() - start_time, 2)))

    try:
        messages_id = [m.message_id for m in messages]
        await bot.delete_messages(messages[-1].chat.id, messages_id)

    except TelegramBadRequest as E:
        print(E)


@group.message(Command("kk", "Kk", "kK", "KK", "кк", "Кк", "кК", "КК"), F.photo)
async def decoding_code(message: Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="upload_photo")
    logger.info(f"@{message.from_user.username} – 'ФОТО'")

    file = await bot.get_file(message.photo[-1].file_id)
    file_path = file.file_path

    current_time = int(time.time())
    user_id = message.from_user.id
    # if user_id == 382202500:
    if user_id == 440055388:
        user_id = "moria"

    image_name = f'{str(user_id)}_{str(current_time)}.jpg'

    await bot.download_file(file_path=file_path, destination=f'./img/assets/decks_img/{image_name}')

    album_builder = MediaGroupBuilder()

    debug_photo_path, role_card_codes, action_card_codes = recognize_deck_img(image_name)
    print(role_card_codes, action_card_codes)
    deck_code = card_codes_to_deck_code(role_card_codes, action_card_codes)

    card_names_str = get_card_name_by_card_code(role_card_codes)
    print(card_names_str)
    print(deck_code)
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

    try:
        await bot.delete_message(message.chat.id, message.message_id)

    except TelegramBadRequest as E:
        print(E)


@group.message(Command("kk", "Kk", "kK", "KK", "кк", "Кк", "кК", "КК"))
async def decoding_code(message: Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

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

            if len(arg) == 3:
                arg2 = arg[2].lower()
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
                await message.answer(caption_text, parse_mode=ParseMode.HTML)
                return

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

                caption_text = (f"{html.bold('для НЕГО: ')}\n - {qw[0]}\n - {qw[1]}\n" + f"{html.bold('для НЕЕ: ')}\n - {qw[2]}\n - {qw[3]}")

                await message.answer(caption_text, parse_mode=ParseMode.HTML)
            return

        if arg1 == 'random' or arg1 == 'r' or arg1 == 'рандом' or arg1 == 'р':
            album_builder = MediaGroupBuilder()
            caption_text = ''

            if len(arg) == 2:
                counter = 1 + 1
            else:
                counter = int(arg[2]) + 1

            for i in range(1, counter):
                generated_deck = generate_deck.get_random_code(card_name_lang='card_name_ru')
                deck_code = generated_deck[0]
                deck_role_cards = generated_deck[1]

                caption_text += (f"{i}) {html.bold(html.quote(deck_role_cards))}\n" +
                                 html.code(html.quote(deck_code)) + "\n")
                photo = create_decks_img(deck_code=deck_code)

                album_builder.add_photo(media=photo, parse_mode=ParseMode.HTML)

            if len(caption_text) < 1000:
                album_builder.caption = caption_text
                await message.reply_media_group(media=album_builder.build())
            else:
                await message.reply_media_group(media=album_builder.build())
                await message.answer(caption_text, parse_mode=ParseMode.HTML)
            return

        if arg1 == 'h' or arg1 == 'hoyolab' or arg1 == 'х' or arg1 == 'хойолаб' or arg1 == 'хуйлаб':
            album_builder = MediaGroupBuilder()
            caption_text = ''

            if len(arg) == 2:
                deck_data = random_hoyolab.get_random_code_from_hoyolab(table_lang='hoyolab_decks_ru')

                author_nickname = deck_data[0]
                role_card_names = deck_data[1]
                deck_code = deck_data[2]
                deck_title = deck_data[3]
                author_uid = deck_data[4]
                description = deck_data[5]
                creation_time = datetime.utcfromtimestamp(int(deck_data[6])).strftime('%Y-%m-%d')
                server = deck_data[7]
                role_cards_codes = deck_data[8]
                action_cards_codes = deck_data[9]

                answer_text = (
                        html.bold(html.quote("🃏 Карты:  ")) + f"{role_card_names}\n\n" +
                        html.bold(html.quote("🏷️ Название:  ")) + f"{deck_title}\n\n" +
                        html.bold(html.quote(
                            "👤 Автор:  ")) + f"{author_nickname}, uid - {html.code(html.quote(author_uid))} ({server}) \n\n" +
                        html.bold(html.quote("🕗 Дата создания:  ")) + f"{creation_time}\n\n" +
                        html.bold(html.quote("📝 Описание:  ")) + f"{description}\n\n" +
                        html.bold(html.quote("#️⃣ Код:  ")) + html.code(html.quote(deck_code)))

                photo = create_decks_img(role_cards=role_cards_codes, action_cards=action_cards_codes)

                caption_len = len(answer_text)

                # 1024 предел
                if caption_len < 1000:
                    await message.reply_photo(photo=photo, caption=answer_text,
                                         parse_mode=ParseMode.HTML)
                    return
                else:
                    await message.reply_photo(photo=photo, parse_mode=ParseMode.HTML)
                    await message.answer(answer_text, parse_mode=ParseMode.HTML)
                    return
            else:
                counter = int(arg[2]) + 1

            for i in range(1, counter):
                deck_data = random_hoyolab.get_random_code_from_hoyolab(table_lang='hoyolab_decks_ru')

                role_card_names = deck_data[1]
                deck_code = deck_data[2]

                caption_text += (f"{i}) {html.bold(html.quote(role_card_names))}\n" +
                                 html.code(html.quote(deck_code)) + "\n")
                photo = create_decks_img(deck_code=deck_code)

                album_builder.add_photo(media=photo, parse_mode=ParseMode.HTML)

            if len(caption_text) < 1000:
                album_builder.caption = caption_text
                await message.reply_media_group(media=album_builder.build())
                return
            else:
                await message.reply_media_group(media=album_builder.build())
                await message.answer(caption_text, parse_mode=ParseMode.HTML)
                return

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

            names_line = get_role_card_names(role_cards=role_cards, lang='ru')
            answer_text = (f"{html.bold(html.quote(names_line))}\n" +
                           html.code(html.quote(deck_code)))

            await message.reply_photo(photo=photo, caption=answer_text, parse_mode=ParseMode.HTML)

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

                names_line = get_role_card_names(role_cards=role_cards, lang='ru')
                answer_text = f"{html.bold(html.quote(names_line))}\n" + html.code(html.quote(deck_code))
                caption_text += str(c) + ') ' + answer_text + '\n'

                album_builder.add_photo(media=photo, parse_mode=ParseMode.HTML)

                if c == 10:
                    break
                c += 1

            if c == 1:
                await message.reply_sticker('CAACAgIAAxkBAAEMdzxmjoaHzm6a5GZ1N6C5ZKbPtOeoCAAC9FgAAgmGeEhYrQGzIHlCKzUE')
                # return
            else:
                album_builder.caption = caption_text
                await message.reply_media_group(media=album_builder.build())
                # return

        if len(result) == 0:
            await message.reply_sticker('CAACAgIAAxkBAAEMdzxmjoaHzm6a5GZ1N6C5ZKbPtOeoCAAC9FgAAgmGeEhYrQGzIHlCKzUE')
            # return

    try:
        await bot.delete_message(message.chat.id, message.message_id)

    except TelegramBadRequest as E:
        print(E)


