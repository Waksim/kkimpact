from datetime import datetime

from aiogram.enums import ParseMode
from aiogram.utils.media_group import MediaGroupBuilder
from loguru import logger

from aiogram import types, Router, F, Bot, html

from functions import random_hoyolab, generate_deck
from functions.create_image import create_decks_img
from keyboards.ua import kb_main_ua
from config import settings
from db.base import KkiDb


bot = Bot(token=settings.bot_token)   # TEST
# bot = Bot(token="<TOKEN_MAIN>")   # MAIN
ua = Router()


# ____________________________________________________________________


@ua.message(F.text.lower() == "🇺🇦 український")
async def cmd_start(message: types.Message):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    database = KkiDb()
    database.set_user_preferences(message.from_user.id, "ua")

    await message.answer_sticker('CAACAgIAAxkBAAELtbNl9Hx92wKQloh3xmrWEiu5Pui-nwACTU4AAmhnoEue0q81egR3KTQE')
    await message.answer("Привіт, Картоботик!\n" +
                         "1) Я можу створювати рандомні деки, або брати їх з Hoyolab.\n" +
                         "Коди колод клікабельні, натисни на них щоб " + html.code(
        "СКОПIЮВАТИ") + " (←клікабельно).\n" +
                         "2) Можеш відправити мені до 10 кодів-колод за раз, я їх розшифрую і надішлю тобі фото і склад.\n\n" +
                         "Надішліть /start або /choose_lang - якщо ви хочете змінити мову\n"
                         , reply_markup=kb_main_ua, parse_mode=ParseMode.HTML)


@ua.message(F.text.lower() == "згенерувати деку")  # 🇺🇦
async def cmd_start(message: types.Message):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    generated_deck = generate_deck.get_random_code(card_name_lang='card_name_ua')
    deck_code = generated_deck[0]
    deck_role_cards = generated_deck[1]

    answer_text = (f"{html.bold(html.quote(deck_role_cards))}\n" +
                   html.code(html.quote(deck_code)))
    photo = create_decks_img(deck_code=deck_code)
    await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=answer_text, parse_mode=ParseMode.HTML,
                         reply_markup=kb_main_ua)


@ua.message(F.text.lower() == "дека з hoyolab")  # 🇺🇦
async def cmd_start(message: types.Message):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    deck_data = random_hoyolab.get_random_code_from_hoyolab(table_lang='hoyolab_decks_ua')

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
            html.bold(html.quote("🃏 Карта:  ")) + f"{role_card_names}\n\n" +
            html.bold(html.quote("🏷️ Назва:  ")) + f"{deck_title}\n\n" +
            html.bold(html.quote(
                "👤 Автор:  ")) + f"{author_nickname}, uid - {html.code(html.quote(author_uid))} ({server}) \n\n" +
            html.bold(html.quote("🕗 Дата створення:  ")) + f"{creation_time}\n\n" +
            html.bold(html.quote("📝 Опис:  ")) + f"{description}\n\n" +
            html.bold(html.quote("#️⃣ Код:  ")) + html.code(html.quote(deck_code)))

    photo = create_decks_img(role_cards=role_cards_codes, action_cards=action_cards_codes)

    caption_len = len(answer_text)
    print(caption_len)
    # 1024 предел
    if caption_len < 1000:
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=answer_text, parse_mode=ParseMode.HTML,
                             reply_markup=kb_main_ua)
    else:
        await bot.send_photo(chat_id=message.chat.id, photo=photo, parse_mode=ParseMode.HTML)
        await message.answer(answer_text, parse_mode=ParseMode.HTML, reply_markup=kb_main_ua)


@ua.message(F.text.regexp(r"^Згенерувати (\d+)$").as_("digits"))  # 🇺🇦
async def cmd_start(message: types.Message, digits: list[str]):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    album_builder = MediaGroupBuilder()
    caption_text = ''
    counter = int(digits[1]) + 1

    for i in range(1, counter):
        generated_deck = generate_deck.get_random_code(card_name_lang='card_name_ua')
        deck_code = generated_deck[0]
        deck_role_cards = generated_deck[1]

        caption_text += (f"{i}) {html.bold(html.quote(deck_role_cards))}\n" +
                         html.code(html.quote(deck_code)) + "\n")
        photo = create_decks_img(deck_code=deck_code)

        album_builder.add_photo(media=photo, parse_mode=ParseMode.HTML)

    if len(caption_text) < 1000:
        album_builder.caption = caption_text
        await message.answer_media_group(media=album_builder.build(), reply_markup=kb_main_ua)
    else:
        await message.answer_media_group(media=album_builder.build())
        await message.answer(caption_text, parse_mode=ParseMode.HTML, reply_markup=kb_main_ua)


@ua.message(F.text.regexp(r"^(\d+) з Hoyolab$").as_("digits"))  # 🇺🇦
async def cmd_start(message: types.Message, digits: list[str]):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    album_builder = MediaGroupBuilder()
    caption_text = ''
    counter = int(digits[1]) + 1

    for i in range(1, counter):
        deck_data = random_hoyolab.get_random_code_from_hoyolab(table_lang='hoyolab_decks_ua')

        role_card_names = deck_data[1]
        deck_code = deck_data[2]

        caption_text += (f"{i}) {html.bold(html.quote(role_card_names))}\n" +
                         html.code(html.quote(deck_code)) + "\n")
        photo = create_decks_img(deck_code=deck_code)

        album_builder.add_photo(media=photo, parse_mode=ParseMode.HTML)

    if len(caption_text) < 1000:
        album_builder.caption = caption_text
        await message.answer_media_group(media=album_builder.build(), reply_markup=kb_main_ua)
    else:
        await message.answer_media_group(media=album_builder.build())
        await message.answer(caption_text, parse_mode=ParseMode.HTML, reply_markup=kb_main_ua)
