import sqlite3
from datetime import datetime

from aiogram.enums import ParseMode
from aiogram.utils.media_group import MediaGroupBuilder
from loguru import logger

from aiogram import types, Router, F, Bot, html

from filters.chat_type import ChatTypeFilter
from functions import random_hoyolab, generate_deck
from functions.create_image import create_decks_img
from keyboards.ru import kb_ru_main
from config import settings


bot = Bot(token=settings.bot_token)

ru = Router()

ru.message.filter(
    ChatTypeFilter(chat_type=["private"])
)


# ____________________________________________________________________


@ru.message(F.text.lower() == "🇷🇺 русский")
async def cmd_start(message: types.Message):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    sqlite_connection = sqlite3.connect('./users_info.sqlite')
    cursor = sqlite_connection.cursor()
    cursor.execute("UPDATE telegram_users SET preferens = 'ru' WHERE tg_id = ?;", (message.from_user.id,))
    sqlite_connection.commit()
    cursor.close()

    await message.answer_sticker('CAACAgIAAxkBAAELtbNl9Hx92wKQloh3xmrWEiu5Pui-nwACTU4AAmhnoEue0q81egR3KTQE')
    await message.answer("Привет, Картоботик!\n" +
                         "1) Я могу создавать рандомные деки, либо брать их с Hoyolab.\n" +
                         "Коды колод кликабельны, нажми на них чтобы " + html.code(
        "СКОПИРОВАТЬ") + " (←кликабельно).\n" +
                         "2) Можешь отправить мне до 10 кодов-колод за раз, я их расшифрую и пришлю тебе фото и состав.\n\n" +
                         "Отправь /start или /choose_lang - если хочешь поменять язык\n"
                         , reply_markup=kb_ru_main, parse_mode=ParseMode.HTML)


# ____________________________________________________________________
@ru.message(F.text.lower() == "сгенерировать деку", flags={"long_operation": "typing"})  # 🇷🇺
async def cmd_start(message: types.Message):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    generated_deck = generate_deck.get_random_code(card_name_lang='card_name_ru')
    deck_code = generated_deck[0]
    deck_role_cards = generated_deck[1]

    answer_text = (f"{html.bold(html.quote(deck_role_cards))}\n" +
                   html.code(html.quote(deck_code)))
    photo = create_decks_img(deck_code=deck_code)
    await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=answer_text, parse_mode=ParseMode.HTML,
                         reply_markup=kb_ru_main)


# ____________________________________________________________________
@ru.message(F.text.lower() == "дека с hoyolab", flags={"long_operation": "typing"})  # 🇷🇺
async def cmd_start(message: types.Message):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

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
    # print(caption_len)
    # 1024 предел
    if caption_len < 1000:
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=answer_text, parse_mode=ParseMode.HTML,
                             reply_markup=kb_ru_main)
    else:
        await bot.send_photo(chat_id=message.chat.id, photo=photo, parse_mode=ParseMode.HTML)
        await message.answer(answer_text, parse_mode=ParseMode.HTML, reply_markup=kb_ru_main)


@ru.message(F.text.regexp(r"^Сгенерировать (\d+)$").as_("digits"), flags={"long_operation": "typing"})  # 🇷🇺
async def cmd_start(message: types.Message, digits: list[str]):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    album_builder = MediaGroupBuilder()
    caption_text = ''
    counter = int(digits[1]) + 1

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
        await message.answer_media_group(media=album_builder.build(), reply_markup=kb_ru_main)
    else:
        await message.answer_media_group(media=album_builder.build())
        await message.answer(caption_text, parse_mode=ParseMode.HTML, reply_markup=kb_ru_main)


@ru.message(F.text.regexp(r"^(\d+) с Hoyolab$").as_("digits"), flags={"long_operation": "typing"})  # 🇷🇺
async def cmd_start(message: types.Message, digits: list[str]):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    album_builder = MediaGroupBuilder()
    caption_text = ''
    counter = int(digits[1]) + 1

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
        await message.answer_media_group(media=album_builder.build(), reply_markup=kb_ru_main)
    else:
        await message.answer_media_group(media=album_builder.build())
        await message.answer(caption_text, parse_mode=ParseMode.HTML, reply_markup=kb_ru_main)
