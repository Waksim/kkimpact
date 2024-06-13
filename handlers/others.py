import re
import sqlite3
from loguru import logger

from aiogram.enums import ParseMode
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram import types, Router, Bot, html
from aiogram.filters.command import Command

from functions import generate_deck
from functions.create_image import create_decks_img
from functions.decryption_of_the_code import decrypt_code
from functions.get_role_card_names import get_role_card_names

# logger.add('telegram_bot.log', level='DEBUG', format="{time:MMM-DD – HH:mm:ss} – {message}", rotation="100 MB",
#            enqueue=True)
bot = Bot(token="7007119455:AAE4UpTzYztO82An8A_1r6rPEw3mWauJ2ps")  # TEST
# bot = Bot(token="7138116207:AAFgEnsCpJ1SavXW0FrvS7rAC-75hT5nYR4")   # MAIN
others = Router()


# ____________________________________________________________________

@others.message(Command('delete_sticker_pack'))
async def cmd_start(message: types.Message):
    sticker_name = 'dendro_by_KKImpact_testBOT'
    result: bool = await bot.delete_sticker_set(sticker_name)
    await message.answer(f"Удален стикерпак: https://t.me/addstickers/{sticker_name}")


@others.message(Command('create_sticker_pack'))
async def cmd_start(message: types.Message):
    # await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    # sticker_id = message.sticker.file_id
    sticker_name = 'geo_by_KKImpact_testBOT'
    # sticker_pack_info = ''

    # time.sleep(10)
    stickers_arr = []

    sqlite_connection = sqlite3.connect('tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()

    cursor.execute("SELECT code, element FROM main.role_cards")
    codes = cursor.fetchall()

    counter = 0

    for code in codes:
        if counter == 49:
            print(counter)
            break
        element = code[1].split(', ')[0]
        if element == 'geo':
            stickers_arr.append(types.InputSticker(sticker=types.FSInputFile(f'img/role_cards_stickers/{code[0]}.png'),
                                                   emoji_list=['🟢']))
            counter += 1

    result: bool = await bot.create_new_sticker_set(user_id=message.from_user.id,
                                                    name=sticker_name,
                                                    title='🌕 GEO 🌕 @KKimpactBOT',
                                                    stickers=stickers_arr,
                                                    sticker_format='static',
                                                    sticker_type='regular'
                                                    )

    await message.answer(f"Создан стикерпак: https://t.me/addstickers/{sticker_name}")


# @others.message(F.sticker)
# async def cmd_start(message: types.Message):
#     sticker_uid = message.sticker.file_unique_id
#     sqlite_connection = sqlite3.connect('tcgCodes.sqlite')
#     cursor = sqlite_connection.cursor()
#     result: bool = await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
#
#     cursor.execute(f"SELECT card_name_ru FROM main.role_cards WHERE sticker_uid = '{sticker_uid}'")
#     r = cursor.fetchall()
#     print(r)
#     if len(r) == 0:
#         message_obj = await message.answer(f"Таких не знаю")
#         print(message_obj)
#     else:
#         card_name = r[0][0]
#
#         cursor.close()
#         # await bot.edit_message_text(text=f"Это {card_name}", chat_id=message.chat.id, message_id=message.message_id-1)
#         message_obj = await message.answer(f"Это {card_name}")
#         print(message_obj)


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


# ____________________________________________________________________


# ____________________________________________________________________
@others.message(Command("generate_text_10"))
async def cmd_start(message: types.Message):
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
async def cmd_start(message: types.Message):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    sqlite_connection = sqlite3.connect('tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()
    tg_id = message.from_user.id
    cursor.execute("SELECT preferens FROM telegram_users where tg_id = ?;", (tg_id,))
    preference = cursor.fetchall()[0][0]

    result = re.findall(r'([^.,\'\"\s\n\t\r]{68})', message.text)

    if len(result) == 1:
        deck_code = result[0]
        decrypted_data = decrypt_code(deck_code)
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

        album_builder.caption = caption_text
        await message.answer_media_group(media=album_builder.build())

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
