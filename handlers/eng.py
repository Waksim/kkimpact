from datetime import datetime

from aiogram.enums import ParseMode
from aiogram.utils.media_group import MediaGroupBuilder
from loguru import logger

from aiogram import types, Router, F, Bot, html

from functions import random_hoyolab, generate_deck
from functions.create_image import create_decks_img
from keyboards.eng import kb_main_eng
from config import settings
from db.base import KkiDb


bot = Bot(token=settings.bot_token)   # TEST
# bot = Bot(token="<TOKEN_MAIN>")   # MAIN
eng = Router()


# ____________________________________________________________________


@eng.message(F.text.lower() == "🇺🇸 english")
async def cmd_start(message: types.Message):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    database = KkiDb()
    database.set_user_preferences(message.from_user.id, "eng")

    await message.answer_sticker('CAACAgIAAxkBAAELtbNl9Hx92wKQloh3xmrWEiu5Pui-nwACTU4AAmhnoEue0q81egR3KTQE')
    await message.answer("Hi, TCG player!\n" +
                         "1) I can create random decks, or take ones from Hoyolab.\n" +
                         "Deck codes are clickable, click on them to " + html.code("COPY") + " (←clickable).\n" +
                         "2) You can send me up to 10 deck codes at a time, I will decrypt them and send you a photo and composition.\n\n" +
                         "Send /start or /choose_lang - if you want to change the language\n"
                         , reply_markup=kb_main_eng, parse_mode=ParseMode.HTML)


@eng.message(F.text.lower() == "generate deck")  # 🇺🇸
async def cmd_start(message: types.Message):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    generated_deck = generate_deck.get_random_code(card_name_lang='card_name_eng')
    deck_code = generated_deck[0]
    deck_role_cards = generated_deck[1]

    answer_text = (f"{html.bold(html.quote(deck_role_cards))}\n" +
                   html.code(html.quote(deck_code)))
    photo = create_decks_img(deck_code=deck_code)
    await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=answer_text, parse_mode=ParseMode.HTML,
                         reply_markup=kb_main_eng)


@eng.message(F.text.lower() == "from hoyolab")  # 🇺🇸
async def cmd_start(message: types.Message):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    deck_data = random_hoyolab.get_random_code_from_hoyolab(table_lang='hoyolab_decks_eng')

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
            html.bold(html.quote("🃏 Cards:  ")) + f"{role_card_names}\n\n" +
            html.bold(html.quote("🏷️ Title:  ")) + f"{deck_title}\n\n" +
            html.bold(html.quote(
                "👤 Author:  ")) + f"{author_nickname}, uid - {html.code(html.quote(author_uid))} ({server}) \n\n" +
            html.bold(html.quote("🕗 Date of creation:  ")) + f"{creation_time}\n\n" +
            html.bold(html.quote("📝 Description:  ")) + f"{description}\n\n" +
            html.bold(html.quote("#️⃣ Code:  ")) + html.code(html.quote(deck_code)))

    photo = create_decks_img(role_cards=role_cards_codes, action_cards=action_cards_codes)

    caption_len = len(answer_text)
    print(caption_len)
    # 1024 предел
    if caption_len < 1000:
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=answer_text, parse_mode=ParseMode.HTML,
                             reply_markup=kb_main_eng)
    else:
        await bot.send_photo(chat_id=message.chat.id, photo=photo, parse_mode=ParseMode.HTML)
        await message.answer(answer_text, parse_mode=ParseMode.HTML, reply_markup=kb_main_eng)


@eng.message(F.text.regexp(r"^Generate (\d+)$").as_("digits"))  # 🇺🇸
async def cmd_start(message: types.Message, digits: list[str]):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    album_builder = MediaGroupBuilder()
    caption_text = ''
    counter = int(digits[1]) + 1

    for i in range(1, counter):
        generated_deck = generate_deck.get_random_code(card_name_lang='card_name_eng')
        deck_code = generated_deck[0]
        deck_role_cards = generated_deck[1]

        caption_text += (f"{i}) {html.bold(html.quote(deck_role_cards))}\n" +
                         html.code(html.quote(deck_code)) + "\n")
        photo = create_decks_img(deck_code=deck_code)

        album_builder.add_photo(media=photo, parse_mode=ParseMode.HTML)

    if len(caption_text) < 1000:
        album_builder.caption = caption_text
        await message.answer_media_group(media=album_builder.build(), reply_markup=kb_main_eng)
    else:
        await message.answer_media_group(media=album_builder.build())
        await message.answer(caption_text, parse_mode=ParseMode.HTML, reply_markup=kb_main_eng)


@eng.message(F.text.regexp(r"^(\d+) from Hoyolab$").as_("digits"))  # 🇺🇸
async def cmd_start(message: types.Message, digits: list[str]):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    album_builder = MediaGroupBuilder()
    caption_text = ''
    counter = int(digits[1]) + 1

    for i in range(1, counter):
        deck_data = random_hoyolab.get_random_code_from_hoyolab(table_lang='hoyolab_decks_eng')

        role_card_names = deck_data[1]
        deck_code = deck_data[2]

        caption_text += (f"{i}) {html.bold(html.quote(role_card_names))}\n" +
                         html.code(html.quote(deck_code)) + "\n")
        photo = create_decks_img(deck_code=deck_code)

        album_builder.add_photo(media=photo, parse_mode=ParseMode.HTML)

    if len(caption_text) < 1000:
        album_builder.caption = caption_text
        await message.answer_media_group(media=album_builder.build(), reply_markup=kb_main_eng)
    else:
        await message.answer_media_group(media=album_builder.build())
        await message.answer(caption_text, parse_mode=ParseMode.HTML, reply_markup=kb_main_eng)
