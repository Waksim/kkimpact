import json
import sqlite3

from aiogram.enums import ParseMode
from aiogram.utils.media_group import MediaGroupBuilder
from loguru import logger

from aiogram import types, Router, F, Bot, html

from filters.chat_type import ChatTypeFilter
from functions.blep_codes_to_kk import blep_codes_to_kk
from functions.create_image import create_decks_img
from functions.decryption_of_the_code import decrypt_code, card_codes_to_deck_code
from functions.get_role_card_names import get_role_card_names
from config import settings
from keyboards.ru import kb_draft_tail_who_win

bot = Bot(token=settings.bot_token)

web_app = Router()

web_app.message.filter(
    ChatTypeFilter(chat_type=["private"])
)


# ____________________________________________________________________
@web_app.message(F.web_app_data)
async def webapp(message: types.Message):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    sqlite_connection = sqlite3.connect('./users_info.sqlite')
    cursor = sqlite_connection.cursor()

    try:
        data = json.loads(message.web_app_data.data)
        your_id = data['your_id']
        opp_id = data['opp_id']
        blep_roles = data['chars_List']
        blep_actions = data['cards_List']

        your_role_cards, your_action_cards = blep_codes_to_kk(blep_roles, blep_actions)
        your_deck_code = card_codes_to_deck_code(your_role_cards, your_action_cards)

        cursor.execute(
            f"SELECT deck_code FROM main.blep_drafts_history WHERE user_id = {opp_id} ORDER BY id DESC LIMIT 1"
        )
        r = cursor.fetchall()
        opp_deck_code = r[0][0]

        if opp_deck_code != '0':
            your_album_builder = MediaGroupBuilder()
            opp_album_builder = MediaGroupBuilder()
            caption_text = ''

            opp_role_cards, opp_action_cards = decrypt_code(opp_deck_code)

            if len(your_role_cards) == 0 and len(your_action_cards) == 0 or len(
                    opp_role_cards) == 0 and len(opp_action_cards):
                await bot.send_message(chat_id=your_id,
                                       text=f"Ваша дека: \n{html.code(html.quote(your_deck_code))}, \nДека оппонента: \n{html.code(html.quote(opp_deck_code))}",
                                       parse_mode=ParseMode.HTML)
                return

            cursor.execute("SELECT preferens FROM telegram_users where tg_id = ?;", (your_id,))
            your_preference = cursor.fetchall()[0][0]
            cursor.execute("SELECT preferens FROM telegram_users where tg_id = ?;", (opp_id,))
            opp_preference = cursor.fetchall()[0][0]

            your_photo = create_decks_img(role_cards=your_role_cards, action_cards=your_action_cards)
            opp_photo = create_decks_img(role_cards=opp_role_cards, action_cards=opp_action_cards)

            your_names_line = get_role_card_names(role_cards=your_role_cards, lang=your_preference)
            opp_names_line = get_role_card_names(role_cards=opp_role_cards, lang=opp_preference)

            your_answer_text = (
                    f"{html.bold(html.quote('😼 Blep - Drafts'))}\n\n{html.bold('Ваша дека:')}\n{html.bold(html.quote(your_names_line))}\n" +
                    html.code(html.quote(
                        your_deck_code)) + f"\n\n{html.bold('Дека оппонента:')} \n" + f"{html.spoiler(html.bold(html.quote(opp_names_line)))}\n" +
                    html.spoiler(html.code(html.quote(opp_deck_code))))
            your_answer_text = (
                    f"{html.bold(html.quote('😼 Blep - Drafts'))}\n\n"
                    f"{html.bold('Ваша дека:')}\n"
                    f"{html.bold(html.quote(your_names_line))}\n"
                    + html.code(html.quote(your_deck_code))
                    + f"\n\n{html.bold('Дека оппонента:')} \n"
                    + html.spoiler(
                        html.bold(html.quote(opp_names_line)) + "\n"
                        + html.code(html.quote(opp_deck_code))
                    )
            )
            opp_answer_text = (
                    f"{html.bold(html.quote('😼 Blep - Drafts'))}\n\n"
                    f"{'Ваша дека:'}\n"
                    f"{html.bold(html.quote(opp_names_line))}\n"
                    + html.code(html.quote(opp_deck_code))
                    + f"\n\n{'Дека оппонента:'} \n"
                    + f"{html.spoiler(html.bold(html.quote(your_names_line)))}\n"
                    + html.spoiler(html.code(html.quote(your_deck_code)))
            )

            your_album_builder.add_photo(media=your_photo, parse_mode=ParseMode.HTML)
            your_album_builder.add_photo(media=opp_photo, parse_mode=ParseMode.HTML, has_spoiler=True)
            your_album_builder.caption = your_answer_text

            opp_album_builder.add_photo(media=opp_photo, parse_mode=ParseMode.HTML)
            opp_album_builder.add_photo(media=your_photo, parse_mode=ParseMode.HTML, has_spoiler=True)
            opp_album_builder.caption = opp_answer_text

            await bot.send_media_group(chat_id=your_id, media=your_album_builder.build())
            await bot.send_media_group(chat_id=opp_id, media=opp_album_builder.build())
            await bot.send_message(chat_id=your_id, text="Конец Драфтов!", reply_markup=kb_draft_tail_who_win(opp_id, 1))
            await bot.send_message(chat_id=opp_id, text="Конец Драфтов!", reply_markup=kb_draft_tail_who_win(your_id, 1))

            cursor.execute(
                f"DELETE FROM main.blep_drafts_history WHERE user_id = {your_id} OR user_id = {opp_id}"
            )
            sqlite_connection.commit()

            logger.info(f"BLEP-Drafts, COOP-Mode\n@{message.from_user.username} – '{your_deck_code}'\n'{opp_deck_code}'")
        else:

            if len(your_role_cards) == 0 and len(your_action_cards) == 0:
                await bot.send_message(chat_id=your_id,
                                       text=f"Ваша дека: {html.code(html.quote(your_deck_code))}, \nДека оппонента: Ожидаем ⌛",
                                       parse_mode=ParseMode.HTML)
                return

            tg_id = message.from_user.id
            cursor.execute("SELECT preferens FROM telegram_users where tg_id = ?;", (tg_id,))
            preference = cursor.fetchall()[0][0]

            photo = create_decks_img(role_cards=your_role_cards, action_cards=your_action_cards)

            names_line = get_role_card_names(role_cards=your_role_cards, lang=preference)
            answer_text = (
                    f"{html.bold(html.quote('😼 Blep - Drafts'))}\n\n{html.bold('Ваша дека:')}\n{html.bold(html.quote(names_line))}\n" +
                    html.code(html.quote(your_deck_code)) + f"\n\n{html.bold('Дека оппонента:')} \nОжидаем ⌛")

            await bot.send_photo(chat_id=your_id, photo=photo, caption=answer_text, parse_mode=ParseMode.HTML)

        cursor.execute(
            f"UPDATE main.blep_drafts_history SET deck_code = '{your_deck_code}' "
            f"WHERE user_id = {your_id}"
        )
        sqlite_connection.commit()

    except json.JSONDecodeError:

        obj = json.loads(message.web_app_data.data)
        blep_role = obj['chars_List']
        blep_action = obj['cards_List']
        role_cards, action_cards = blep_codes_to_kk(blep_role, blep_action)
        deck_code = card_codes_to_deck_code(role_cards, action_cards)

        logger.info(f"@{message.from_user.username} – BLEP-Draft: '{deck_code}'")

        if len(role_cards) == 0 and len(action_cards) == 0:
            await message.reply_sticker('CAACAgIAAxkBAAEMdzxmjoaHzm6a5GZ1N6C5ZKbPtOeoCAAC9FgAAgmGeEhYrQGzIHlCKzUE')
            return

        card_codes_to_deck_code(role_cards)
        sqlite_connection = sqlite3.connect('./users_info.sqlite')
        cursor = sqlite_connection.cursor()
        tg_id = message.from_user.id
        cursor.execute("SELECT preferens FROM telegram_users where tg_id = ?;", (tg_id,))
        preference = cursor.fetchall()[0][0]

        photo = create_decks_img(role_cards=role_cards, action_cards=action_cards)

        names_line = get_role_card_names(role_cards=role_cards, lang=preference)
        answer_text = (f"{html.bold(html.quote('😼 Blep - Drafts'))}\n{html.bold(html.quote(names_line))}\n" +
                       html.code(html.quote(deck_code)))

        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=answer_text, parse_mode=ParseMode.HTML)
