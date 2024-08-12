import sqlite3
from datetime import datetime

import content as content
from aiogram.enums import ParseMode
from aiogram.utils.media_group import MediaGroupBuilder
from loguru import logger
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from aiogram import types, Router, F, Bot, html

from filters.chat_type import ChatTypeFilter
from functions import random_hoyolab, generate_deck
from functions.create_image import create_decks_img
from functions.decryption_of_the_code import decrypt_code
from functions.get_role_card_names import get_role_card_names
from keyboards.ru import kb_ru_main
from config import settings

bot = Bot(token=settings.bot_token)

web_app = Router()

web_app.message.filter(
    ChatTypeFilter(chat_type=["private"])
)


# ____________________________________________________________________
@web_app.message(F.web_app_data)
async def webapp(message: types.Message):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")

    deck_code = message.web_app_data.data

    logger.info(f"@{message.from_user.username} – BLEP-Draft: '{deck_code}'")

    decrypted_data = decrypt_code(deck_code)

    if len(decrypted_data[0]) == 0 and len(decrypted_data[1]) == 0:
        await message.reply_sticker('CAACAgIAAxkBAAEMdzxmjoaHzm6a5GZ1N6C5ZKbPtOeoCAAC9FgAAgmGeEhYrQGzIHlCKzUE')
        return

    sqlite_connection = sqlite3.connect('./users_info.sqlite')
    cursor = sqlite_connection.cursor()
    tg_id = message.from_user.id
    cursor.execute("SELECT preferens FROM telegram_users where tg_id = ?;", (tg_id,))
    preference = cursor.fetchall()[0][0]

    role_cards = decrypted_data[0]
    action_cards = decrypted_data[1]

    photo = create_decks_img(role_cards=role_cards, action_cards=action_cards)

    names_line = get_role_card_names(role_cards=role_cards, lang=preference)
    answer_text = (f"{html.bold(html.quote('😼 Blep - Drafts'))}\n{html.bold(html.quote(names_line))}\n" +
                   html.code(html.quote(deck_code)))

    await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=answer_text, parse_mode=ParseMode.HTML)
