import json
import random
import sqlite3
import time
from datetime import datetime

from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ReplyKeyboardRemove, InputMediaPhoto
from loguru import logger

from aiogram import types, Router, F, Bot, html, Dispatcher

from functions.create_image import create_draft_tail_img
from functions.find_resonance import find_resonance
from functions.get_card_name_by_sticker import get_card_number_by_sticker
from keyboards.cn import kb_main_cn
from keyboards.eng import kb_main_eng
from keyboards.ru import kb_draft_queue, kb_draft_tail_accept_decline, kb_draft_tail_who_win
from keyboards.ru import kb_ru_main, kb_draft_tail
from keyboards.ua import kb_main_ua
from config import settings


bot = Bot(token=settings.bot_token)   # TEST
# bot = Bot(token="<TOKEN_MAIN>")   # MAIN
drafts_tail = Router()
dp = Dispatcher()


async def create_draft_answer(your_status, draft_data=None):
    if draft_data is not None:
        first_picks_string = ', '.join(draft_data[0])
        first_bans_string = ', '.join(draft_data[1])
        second_picks_string = ', '.join(draft_data[2])
        second_bans_string = ', '.join(draft_data[3])

        answer = (
                f"{html.bold('ДРАФТЫ:')}\n\n"
                f"{html.bold('Баны: ')}\n1) " + first_bans_string + "\n"
                                                                    f"2) " + second_bans_string + "\n\n"
                                                                                                  f"{html.bold('Пики: ')}\n1) " + first_picks_string + "\n"
                                                                                                                                                       f"2) " + second_picks_string + "\n\n"
                + html.bold(html.underline(your_status))
        )

        return answer
    else:
        answer = (
                f"{html.bold('ДРАФТЫ:')}\n\n"
                f"{html.bold('Баны: ')}\n1) \n"
                f"2) \n\n"
                f"{html.bold('Пики: ')}\n1) \n"
                f"2) \n\n"
                + html.bold(html.underline(your_status))
        )
        return answer


def create_queue_answer(users_data, user_id):
    queue_answer = f"{html.bold('Список игроков в подборе:')}\n\n"
    # queue_answer += f"1) BOT, @KKimpactBot\n"
    counter = 0
    requested = []
    for user in users_data:
        if user[0] == user_id:
            if user[4] is not None:
                requested = json.loads(user[4])
    if len(users_data) > 1:
        for user in users_data:
            if user[0] == user_id:
                continue
            username = user[2]
            firstname = user[3]

            clock = ''
            if str(user[0]) in requested:
                clock = '⏳'

            counter += 1
            if username == 'None':
                queue_answer += f"{counter}) {firstname}, {html.link('ССЫЛКА', f'https://web.telegram.org/k/#{user[0]}')}, {html.link('ССЫЛКА', f'tg://user?id={user[0]}')} {clock}\n"
                # queue_answer += f"{counter}) {firstname}, {html.link('ССЫЛКА', f'tg://user?id={user[0]}')} {clock}\n"
                print(queue_answer)
            else:
                queue_answer += f"{counter}) {firstname}, @{username} {clock}\n"
    else:
        queue_answer += 'пусто'
    return queue_answer


async def update_queue():
    sqlite_connection = sqlite3.connect('tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()
    cursor.execute(
        f"SELECT user_id, message_id, username, firstname, requested FROM main.draft_tail_queue WHERE in_the_queue = 1"
    )
    users_data = cursor.fetchall()

    if len(users_data) > 0:
        for user in users_data:
            user_id = user[0]
            message_id = user[1]
            queue_answer = create_queue_answer(users_data=users_data, user_id=user_id)

            try:
                await bot.edit_message_text(
                    text=queue_answer, chat_id=user_id,
                    message_id=message_id,
                    parse_mode=ParseMode.HTML,
                    reply_markup=kb_draft_queue(users_data, user_id),
                    disable_web_page_preview=True
                )
            except TelegramBadRequest:
                pass

    else:
        return


# ____________________________________________________________________
@drafts_tail.message(F.text.lower() == "🦊 драфты хвост")
async def show_draft_menu(message: types.Message, state: FSMContext):
    logger.info(f"@{message.from_user.username} – '{message.text}'")
    sqlite_connection = sqlite3.connect('tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()

    cursor.execute(
        "SELECT EXISTS(SELECT * FROM main.draft_tail_queue where user_id = ?)", (message.from_user.id,)
    )
    in_queue = cursor.fetchall()[0][0]
    if in_queue == 0:
        cursor.execute(
            f"INSERT INTO main.draft_tail_queue (user_id, username, firstname) "
            f"VALUES (?, ?, ?)",
            (message.from_user.id, message.from_user.username, message.from_user.first_name)
        )
        sqlite_connection.commit()

    cursor.execute(f"SELECT user_id, message_id, username, firstname, requested FROM main.draft_tail_queue "
                   f"WHERE in_the_queue = 1")
    users_data = cursor.fetchall()

    if len(users_data) > 0:
        queue_answer = create_queue_answer(users_data, message.from_user.id)
    else:
        queue_answer = f"Список игроков в подборе:\n\n"
        # queue_answer = f"Список игроков в подборе:\n\n1) BOT, @KKimpactBot\n"

    await message.answer(text='👥', reply_markup=ReplyKeyboardRemove())

    message_obj = await message.answer(
        queue_answer,
        parse_mode=ParseMode.HTML,
        reply_markup=kb_draft_queue(users_data, message.from_user.id),
        disable_web_page_preview=True
    )
    cursor.execute(
        "UPDATE main.draft_tail_queue SET datatime = ?, message_id = ? WHERE user_id = ?",
        (int(datetime.now().timestamp()), message_obj.message_id, message.from_user.id)
    )
    sqlite_connection.commit()

    await update_queue()


@drafts_tail.callback_query(F.data == "choose_opponent_alert")
async def choose_opponent_alert(callback: types.CallbackQuery):
    await callback.answer(
        text="Выберите пользователя из списка ниже, с которым хотите сыграть в драфты и нажмите на соответствующую кнопку.",
        show_alert=True
    )


@drafts_tail.callback_query(F.data == "update_queue_list")
async def update_queue_list(callback: types.CallbackQuery):
    sqlite_connection = sqlite3.connect('tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()
    user_id = callback.from_user.id
    message_id = callback.message.message_id

    cursor.execute(f"SELECT user_id, message_id, username, firstname, requested FROM main.draft_tail_queue "
                   f"WHERE in_the_queue = 1")
    users_data = cursor.fetchall()

    if len(users_data) > 0:
        queue_answer = create_queue_answer(users_data, callback.from_user.id)
    else:
        queue_answer = f"Список игроков в подборе:\n\nпусто"

    try:
        await bot.edit_message_text(
            text=queue_answer, chat_id=user_id,
            message_id=message_id,
            parse_mode=ParseMode.HTML,
            reply_markup=kb_draft_queue(users_data, user_id)
        )
    except TelegramBadRequest:
        pass

    await callback.answer()


@drafts_tail.callback_query(F.data == "go_to_main_menu")
async def go_to_main_menu(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    message = callback.message
    message_id = message.message_id
    result: bool = await bot.delete_message(chat_id=user_id, message_id=message_id)
    try:
        result: bool = await bot.delete_message(chat_id=user_id, message_id=message_id - 1)
    except TelegramBadRequest:
        pass

    sqlite_connection = sqlite3.connect('tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()
    cursor.execute("SELECT preferens FROM telegram_users where tg_id = ?;", (user_id,))
    preference = cursor.fetchall()[0][0]

    await message.answer_sticker('CAACAgIAAxkBAAELtbNl9Hx92wKQloh3xmrWEiu5Pui-nwACTU4AAmhnoEue0q81egR3KTQE')
    if preference == 'cn':
        await message.answer("嗨!\n" +
                             "1) 我可以创建随机卡片组，或者从Hoyolab中获取它们。\n" +
                             "甲板代码是可点击的,点击他们 " + html.code("复制") + " (←可点击).\n" +
                             "2）您可以一次给我发送最多10个甲板代码，我会解密它们并向您发送照片和构图。\n\n" +
                             "发送 /start 或 /choose_lang - 如果你想改变语言\n"
                             , reply_markup=kb_main_cn, parse_mode=ParseMode.HTML)
    if preference == 'eng':
        await message.answer("Hi, TCG player!\n" +
                             "1) I can create random decks, or take ones from Hoyolab.\n" +
                             "Deck codes are clickable, click on them to " + html.code("COPY") + " (←clickable).\n" +
                             "2) You can send me up to 10 deck codes at a time, I will decrypt them and send you a photo and composition.\n\n" +
                             "Send /start or /choose_lang - if you want to change the language\n"
                             , reply_markup=kb_main_eng, parse_mode=ParseMode.HTML)
    if preference == 'ua':
        await message.answer("Привіт, Картоботик!\n" +
                             "1) Я можу створювати рандомні деки, або брати їх з Hoyolab.\n" +
                             "Коди колод клікабельні, натисни на них щоб " + html.code(
            "СКОПIЮВАТИ") + " (←клікабельно).\n" +
                             "2) Можеш відправити мені до 10 кодів-колод за раз, я їх розшифрую і надішлю тобі фото і склад.\n\n" +
                             "Надішліть /start або /choose_lang - якщо ви хочете змінити мову\n"
                             , reply_markup=kb_main_ua, parse_mode=ParseMode.HTML)
    if preference == 'ru':
        await message.answer("Привет, Картоботик!\n" +
                             "1) Я могу создавать рандомные деки, либо брать их с Hoyolab.\n" +
                             "Коды колод кликабельны, нажми на них чтобы " + html.code(
            "СКОПИРОВАТЬ") + " (←кликабельно).\n" +
                             "2) Можешь отправить мне до 10 кодов-колод за раз, я их расшифрую и пришлю тебе фото и состав.\n\n" +
                             "Отправь /start или /choose_lang - если хочешь поменять язык\n"
                             , reply_markup=kb_ru_main, parse_mode=ParseMode.HTML)

    sqlite_connection = sqlite3.connect('tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()

    cursor.execute(
        f"DELETE FROM main.draft_tail_queue WHERE user_id = {user_id}"
    )
    sqlite_connection.commit()

    await update_queue()

    await callback.answer()

    await state.clear()


@drafts_tail.callback_query(F.data.startswith("draft_tail_request="))
async def draft_tail_request(callback: types.CallbackQuery):
    user_id_1 = callback.from_user.id
    username_1 = callback.from_user.username
    firstname_1 = callback.from_user.first_name
    user_id_2 = callback.data.split("=")[1]

    sqlite_connection = sqlite3.connect('tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()
    cursor.execute(f"SELECT requested FROM main.draft_tail_queue WHERE user_id = {user_id_1}")
    requested = cursor.fetchall()[0][0]
    # print(requested)
    if requested is None:
        # print('is none')
        requested = [user_id_2]
        requested = json.dumps(requested)
        cursor.execute(
            f"UPDATE main.draft_tail_queue SET requested = '{requested}' WHERE user_id = {user_id_1}"
        )
        sqlite_connection.commit()

        await bot.send_message(
            chat_id=user_id_2,
            text=f"Пользователь {firstname_1}, @{username_1}: приглашает вас сыграть в драфты.",
            reply_markup=kb_draft_tail_accept_decline(user_id_1, username_1)
        )
        await update_queue()
        return

    requested_json_load = json.loads(requested)
    if str(user_id_2) in requested_json_load:
        await bot.answer_callback_query(
            callback_query_id=callback.id,
            text=f"Вы уже отправили запрос этому пользователю!",
            show_alert=True
        )
        return
    elif str(user_id_2) not in requested_json_load:
        requested = requested_json_load
        requested.append(user_id_2)
        requested = json.dumps(requested)
        # print(requested)
        cursor.execute(
            f"UPDATE main.draft_tail_queue SET requested = '{requested}' WHERE user_id = {user_id_1}"
        )
        sqlite_connection.commit()

        await bot.send_message(
            chat_id=user_id_2,
            text=f"Пользователь {firstname_1}, @{username_1}: приглашает вас сыграть в драфты.",
            reply_markup=kb_draft_tail_accept_decline(user_id_1, username_1)
        )
        await update_queue()


@drafts_tail.callback_query(F.data.startswith("draft_tail_declined="))
async def draft_tail_declined(callback: types.CallbackQuery):
    user_id = callback.data.split("=")[1]
    message_obj = await bot.send_message(
        chat_id=user_id,
        text=f"Пользователь {callback.from_user.first_name} отклонил ваш запрос",
    )
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    time.sleep(5)
    await bot.delete_message(
        chat_id=user_id,
        message_id=message_obj.message_id
    )


@drafts_tail.callback_query(F.data.startswith("draft_tail_accepted="))
async def draft_tail_accepted(callback: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    user_id_1 = int(callback.data.splitw("=")[1])
    username_1 = callback.data.split("=")[2]
    user_id_2 = int(callback.from_user.id)
    username_2 = callback.from_user.username
    sqlite_connection = sqlite3.connect('tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()

    first_player = dict()
    first_player['user_id'] = user_id_1  # callback.from_user.id
    first_player['nickname'] = '@' + username_1
    first_player['opponent'] = user_id_2  # callback.data.split("=")[1]
    first_player['picks'] = json.dumps([])
    first_player['bans'] = json.dumps([])

    second_player = dict()
    second_player['user_id'] = user_id_2  # callback.data.split("=")[1]
    second_player['nickname'] = '@' + username_2
    second_player['opponent'] = user_id_1  # callback.from_user.id
    second_player['picks'] = json.dumps([])
    second_player['bans'] = json.dumps([])

    first_player['first_pick'] = random.choice([0, 1])
    if first_player['first_pick'] == 0:
        second_player['first_pick'] = 1
    else:
        second_player['first_pick'] = 0

    for current_player in first_player, second_player:
        if current_player['first_pick'] == 0:
            nickname2 = current_player['nickname']
        else:
            nickname1 = current_player['nickname']
    filename = str(first_player['user_id'] + second_player['user_id'])
    photo = create_draft_tail_img(99, None, filename, nickname1, nickname2)
    # photo = BufferedInputFile(photo, filename="file.txt")

    for current_player in first_player, second_player:
    # for current_player in [first_player]:
        if current_player['first_pick'] == 0:
            draft_answer = await create_draft_answer('БАН ПРОТИВНИКА')
            message_obj = await bot.send_photo(
                chat_id=current_player['user_id'],
                caption=draft_answer,
                parse_mode=ParseMode.HTML,
                reply_markup=kb_draft_tail,
                photo=photo
            )
        else:
            draft_answer = await create_draft_answer('ВАШ БАН')
            message_obj = await bot.send_photo(
                chat_id=current_player['user_id'],
                caption=draft_answer,
                parse_mode=ParseMode.HTML,
                reply_markup=kb_draft_tail,
                photo=photo
            )
        # print(message_obj)
        current_player['message_id'] = message_obj.message_id
        print(current_player['message_id'])
        cursor.execute(
            f"INSERT INTO main.draft_tail (user_id, message_id, first_pick, datatime, opponent, stage)"
            f"VALUES (?, ?, ?, ?, ?, ?)",
            (current_player['user_id'], current_player['message_id'], current_player['first_pick'],
             int(datetime.now().timestamp()), current_player['opponent'], 0)
        )
        sqlite_connection.commit()

        cursor.execute(
            f"UPDATE main.draft_tail_queue SET requested = NULL, in_the_queue = 0 "
            f"WHERE user_id = {current_player['user_id']}"
        )
        sqlite_connection.commit()

    await state.set_state('DraftTail')


async def add_new_card_to_drafts_data(card_code, bans_or_picks, bans_or_picks_arr, user_id, draft_data):
    card_name = get_name_card_by_code(card_code)
    draft_data_in_row = []
    for draft_data_row in draft_data:
        if len(draft_data_row) != 0:
            for data in draft_data_row:
                draft_data_in_row.append(data)
    # print('draft_data_in_row--- ', draft_data_in_row)
    if card_name not in draft_data_in_row:
        sqlite_connection = sqlite3.connect('tcgCodes.sqlite')
        cursor = sqlite_connection.cursor()

        bans_or_picks_arr.append(card_code)
        json_str = json.dumps(bans_or_picks_arr)

        cursor.execute(
            f"UPDATE main.draft_tail SET {bans_or_picks} = '{json_str}' WHERE user_id = {user_id}"
        )
        sqlite_connection.commit()
        return draft_data
    else:
        return 0


async def stage_update(stage, user_id):
    sqlite_connection = sqlite3.connect('tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()

    cursor.execute(
        f"UPDATE main.draft_tail SET stage = '{stage}' WHERE user_id = {user_id}"
    )
    sqlite_connection.commit()


def get_name_card_by_code(code_card):
    sqlite_connection = sqlite3.connect('tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()
    cursor.execute(
        f"SELECT card_name_ru FROM main.role_cards WHERE code = {code_card}"
    )
    r = cursor.fetchall()
    card_name = r[0][0]
    return card_name


async def update_drafts(user_id_1, user_id_2, fp_status, scp_status, stage, cardcode):
    sqlite_connection = sqlite3.connect('tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()

    draft_data = []
    message_ids = []  # usr1, usr2

    picks = []

    for user_id in (user_id_1, user_id_2):
        cursor.execute(
            f"SELECT message_id, picks, bans FROM main.draft_tail WHERE user_id = {user_id} ORDER BY id DESC"
        )
        r = cursor.fetchall()
        if len(r) == 0:
            draft_data.append([])
            draft_data.append([])
        else:
            r = r[0]
            message_ids.append(r[0])
            codes_picks = json.loads(r[1])
            codes_bans = json.loads(r[2])
            names_picks = []
            names_bans = []
            for code_pick in codes_picks:
                names_picks.append(get_name_card_by_code(code_pick))
            for code_ban in codes_bans:
                names_bans.append(get_name_card_by_code(code_ban))

            picks.append(codes_picks)
            draft_data.append(names_picks)
            draft_data.append(names_bans)

    users_ids = [user_id_1, user_id_2]
    c = 0
    resonances = []
    for pick in picks:
        resonances.append(find_resonance(pick))
    photo = create_draft_tail_img(stage, cardcode, user_id_1+user_id_2, resonance1=resonances[0], resonance2=resonances[1])

    for status in [fp_status, scp_status]:
        draft_answer = await create_draft_answer(status, draft_data)
        media_photo = InputMediaPhoto(media=photo, caption=draft_answer, parse_mode=ParseMode.HTML)
        message_obj = await bot.edit_message_media(
            chat_id=users_ids[c],
            message_id=message_ids[c],
            reply_markup=kb_draft_tail,
            media=media_photo
        )

        cursor.execute(
            f"UPDATE main.draft_tail SET draft_data = '{json.dumps(draft_data)}' WHERE user_id = {users_ids[c]}"
        )
        sqlite_connection.commit()

        c += 1

    # print(draft_data)


async def draft_error(error_text, message):
    message_obj = await bot.send_message(
        text=error_text, chat_id=message.from_user.id
    )
    time.sleep(2)
    await bot.delete_message(chat_id=message.chat.id, message_id=message_obj.message_id)


# @drafts_tail.message(F.sticker, StateFilter('DraftTail'))
@drafts_tail.message(F.sticker)
async def show_draft_menu(message: types.Message, state: FSMContext):
    result: bool = await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    sticker_uid = message.sticker.file_unique_id

    sqlite_connection = sqlite3.connect('tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()

    cursor.execute(
        f"SELECT user_id, message_id, picks, bans, first_pick, opponent, stage, draft_data"
        f" FROM main.draft_tail WHERE user_id = '{message.from_user.id}'"
        f"ORDER BY id DESC"
    )
    r = cursor.fetchall()
    if len(r) != 0:
        r = r[0]
        user_id = r[0]
        message_id = r[1]
        picks = json.loads(r[2])
        bans = json.loads(r[3])
        first_pick = r[4]
        opponent = r[5]
        stage = r[6]
        draft_data = json.loads(r[7])
        card_code = await get_card_number_by_sticker(sticker_uid)
        if card_code == 0:
            await draft_error(error_text='ОШИБКА! Я не знаю такой стикер!', message=message)

        if stage == 0:
            # 1 бан I игрока
            if first_pick:
                # print('1 бан I игрока')
                if await add_new_card_to_drafts_data(card_code, 'bans', bans, user_id, draft_data):
                    await update_drafts(
                        user_id, opponent, fp_status='БАН ПРОТИВНИКА', scp_status='ВАШ БАН', stage=stage, cardcode=card_code)
                    await stage_update(1, user_id)
                    await stage_update(1, opponent)
                else:
                    # карта уже есть в драфтах
                    await draft_error(error_text='неизвестная ошибка, отправьте скриншот @maksenro', message=message)
            else:
                # ожидаем 1 бана I игрока
                await draft_error(error_text='ОШИБКА! Сейчас бан противника!', message=message)

        if stage == 1:
            # 1 бан II игрока
            if first_pick:
                # ожидаем 1 бана II игрока
                await draft_error(error_text='ОШИБКА! Сейчас бан противника!', message=message)
            else:
                # print('1 бан II игрока')
                if await add_new_card_to_drafts_data(card_code, 'bans', bans, user_id, draft_data):
                    await update_drafts(
                        opponent, user_id, fp_status='ПИК ПРОТИВНИКА', scp_status='ВАШ ПИК', stage=stage, cardcode=card_code)
                    await stage_update(2, user_id)
                    await stage_update(2, opponent)
                else:
                    # карта уже есть в драфтах
                    await draft_error(error_text='ОШИБКА! Повтор карты, проверьте пики и баны!', message=message)

        if stage == 2:
            # 1 пик II игрока
            if first_pick:
                # ожидаем 1 пик II игрока
                await draft_error(error_text='ОШИБКА! Сейчас пик противника!', message=message)
            else:
                # print('1 бан II игрока')
                if await add_new_card_to_drafts_data(card_code, 'picks', picks, user_id, draft_data):
                    await update_drafts(
                        opponent, user_id, fp_status='ВАШ БАН', scp_status='БАН ПРОТИВНИКА', stage=stage, cardcode=card_code)
                    await stage_update(3, user_id)
                    await stage_update(3, opponent)
                else:
                    # карта уже есть в драфтах
                    await draft_error(error_text='ОШИБКА! Повтор карты, проверьте пики и баны!', message=message)

        if stage == 3:
            # 2 бан I игрока
            if first_pick:
                if await add_new_card_to_drafts_data(card_code, 'bans', bans, user_id, draft_data):
                    await update_drafts(
                        user_id, opponent, fp_status='ВАШ ПИК', scp_status='ПИК ПРОТИВНИКА', stage=stage, cardcode=card_code)
                    await stage_update(4, user_id)
                    await stage_update(4, opponent)
                else:
                    # карта уже есть в драфтах
                    await draft_error(error_text='ОШИБКА! Повтор карты, проверьте пики и баны!', message=message)
            else:
                # ожидаем 2 бан I игрока
                await draft_error(error_text='ОШИБКА! Сейчас бан противника!', message=message)

        if stage == 4:
            # 1 пик I игрока
            if first_pick:
                if await add_new_card_to_drafts_data(card_code, 'picks', picks, user_id, draft_data):
                    await update_drafts(
                        user_id, opponent, fp_status='БАН ПРОТИВНИКА', scp_status='ВАШ БАН', stage=stage, cardcode=card_code)
                    await stage_update(5, user_id)
                    await stage_update(5, opponent)
                else:
                    # карта уже есть в драфтах
                    await draft_error(error_text='ОШИБКА! Повтор карты, проверьте пики и баны!', message=message)
            else:
                # ожидаем 1 пик I игрока
                await draft_error(error_text='ОШИБКА! Сейчас пик противника!', message=message)

        if stage == 5:
            # 2 бан II игрока
            if first_pick:
                # ожидаем 2 бана II игрока
                await draft_error(error_text='ОШИБКА! Сейчас бан противника!', message=message)
            else:
                if await add_new_card_to_drafts_data(card_code, 'bans', bans, user_id, draft_data):
                    await update_drafts(
                        opponent, user_id, fp_status='ПИК ПРОТИВНИКА', scp_status='ВАШ ПИК', stage=stage, cardcode=card_code)
                    await stage_update(6, user_id)
                    await stage_update(6, opponent)
                else:
                    # карта уже есть в драфтах
                    await draft_error(error_text='ОШИБКА! Повтор карты, проверьте пики и баны!', message=message)

        if stage == 6:
            # 2 пик II игрока
            if first_pick:
                # ожидаем 2 пик II игрока
                await draft_error(error_text='ОШИБКА! Сейчас пик противника!', message=message)
            else:
                if await add_new_card_to_drafts_data(card_code, 'picks', picks, user_id, draft_data):
                    await update_drafts(
                        opponent, user_id, fp_status='ВАШ ПИК', scp_status='ПИК ПРОТИВНИКА', stage=stage, cardcode=card_code)
                    await stage_update(7, user_id)
                    await stage_update(7, opponent)
                else:
                    # карта уже есть в драфтах
                    await draft_error(error_text='ОШИБКА! Повтор карты, проверьте пики и баны!', message=message)

        if stage == 7:
            # 2 пик I игрока
            if first_pick:
                if await add_new_card_to_drafts_data(card_code, 'picks', picks, user_id, draft_data):
                    await update_drafts(
                        user_id, opponent, fp_status='ВАШ ПИК', scp_status='ПИК ПРОТИВНИКА', stage=stage, cardcode=card_code)
                    await stage_update(8, user_id)
                    await stage_update(8, opponent)
                else:
                    # карта уже есть в драфтах
                    await draft_error(error_text='ОШИБКА! Повтор карты, проверьте пики и баны!', message=message)
            else:
                # ожидаем 2 пик I игрока
                await draft_error(error_text='ОШИБКА! Сейчас пик противника!', message=message)

        if stage == 8:
            # 3 пик I игрока
            if first_pick:
                if await add_new_card_to_drafts_data(card_code, 'picks', picks, user_id, draft_data):
                    await update_drafts(
                        user_id, opponent, fp_status='ПИК ПРОТИВНИКА', scp_status='ВАШ ПИК', stage=stage, cardcode=card_code)
                    await stage_update(9, user_id)
                    await stage_update(9, opponent)
                else:
                    # карта уже есть в драфтах
                    await draft_error(error_text='ОШИБКА! Повтор карты, проверьте пики и баны!', message=message)
            else:
                # ожидаем 3 пик I игрока
                await draft_error(error_text='ОШИБКА! Сейчас пик противника!', message=message)

        if stage == 9:
            # 3 пик II игрока
            if first_pick:
                # ожидаем 3 пик II игрока
                await draft_error(error_text='ОШИБКА! Сейчас пик противника!', message=message)
            else:
                if await add_new_card_to_drafts_data(card_code, 'picks', picks, user_id, draft_data):
                    draft_data = []
                    message_ids = []  # usr1, usr2
                    fp_status = 'КОНЕЦ ДРАФТОВ'
                    scp_status = 'КОНЕЦ ДРАФТОВ'
                    picks = []
                    users_ids = [user_id, opponent]
                    opponent_ids = [opponent, user_id]

                    for user_id in users_ids:
                        cursor.execute(
                            f"SELECT message_id, picks, bans FROM main.draft_tail WHERE user_id = {user_id} ORDER BY id DESC"
                        )
                        r = cursor.fetchall()
                        if len(r) == 0:
                            draft_data.append([])
                            draft_data.append([])
                        else:
                            r = r[0]
                            message_ids.append(r[0])
                            codes_picks = json.loads(r[1])
                            codes_bans = json.loads(r[2])
                            names_picks = []
                            names_bans = []
                            for code_pick in codes_picks:
                                names_picks.append(get_name_card_by_code(code_pick))
                            for code_ban in codes_bans:
                                names_bans.append(get_name_card_by_code(code_ban))

                            picks.append(codes_picks)
                            draft_data.append(names_picks)
                            draft_data.append(names_bans)

                    c = 0
                    resonances = []
                    for pick in picks:
                        resonances.append(find_resonance(pick))
                    photo = create_draft_tail_img(stage, card_code, users_ids[0] + users_ids[1], resonance1=resonances[1],
                                                  resonance2=resonances[0])

                    for status in [fp_status, scp_status]:
                        draft_answer = await create_draft_answer(status, draft_data)
                        media_photo = InputMediaPhoto(media=photo, caption=draft_answer, parse_mode=ParseMode.HTML)
                        message_obj = await bot.edit_message_media(
                            chat_id=users_ids[c],
                            message_id=message_ids[c],
                            reply_markup=kb_draft_tail_who_win(opponent_ids[c]),
                            media=media_photo
                        )
                        c += 1

                    cursor.execute(
                        f"INSERT INTO main.draft_tail_history (user_id, datatime, first_pick, opponent, draft_data) VALUES (?, ?, ?, ?, ?)", (users_ids[0], int(datetime.now().timestamp()), 0, users_ids[1], json.dumps(draft_data))
                    )
                    sqlite_connection.commit()
                    cursor.execute(
                        f"INSERT INTO main.draft_tail_history (user_id, datatime, first_pick, opponent, draft_data) VALUES (?, ?, ?, ?, ?)", (users_ids[1], int(datetime.now().timestamp()), 1, users_ids[0], json.dumps(draft_data))
                    )
                    sqlite_connection.commit()
                    cursor.execute(
                        f"DELETE FROM main.draft_tail WHERE user_id = {users_ids[0]} OR user_id = {users_ids[1]}"
                    )
                    sqlite_connection.commit()

                    logger.info(f"@{message.from_user.username} – DRAFTS EDN")

                else:
                    # карта уже есть в драфтах
                    await draft_error(error_text='ОШИБКА! Повтор карты, проверьте пики и баны!', message=message)

        if stage == 10:
            print('Последний пик противника')

    else:
        await message.answer(
            text='Ваши драфты удалены тк прошло больше 24ч с момента их начала', reply_markup=kb_ru_main
        )

    # draft_answer = create_draft_answer()
    # message_obj = await message.answer(
    #     draft_answer,
    #     parse_mode=ParseMode.HTML,
    #     disable_web_page_preview=True,
    #     reply_markup=kb_draft_tail
    # )
    # await state.set_state(DraftTail.enemy_ban)
    # await state.update_data(drafts_message_id=message_obj.message_id)


@drafts_tail.callback_query(F.data == "draft_tail_rules")
async def show_draft_menu(callback: types.CallbackQuery):
    await bot.answer_callback_query(
        callback_query_id=callback.id,
        text=f"Порядок драфтов:\n1) бан\n2) бан, пик\n1) бан, пик\n2) бан, пик\n1) пик, пик\n2) пик\n\n"
             f"Когда ваш ход, нажмите на кнопку с нужной стихией и отправьте боту стикер персонажа которого "
             f"вы хотите пикнуть/забанить!",
        show_alert=True
    )


def random_cardcode(draft_data):
    sqlite_connection = sqlite3.connect('tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()

    cursor.execute(
        "SELECT code FROM main.role_cards"
    )
    r = cursor.fetchall()
    codes = []
    for code in r:
        codes.append(code[0])
    print(codes)
    if draft_data == 0:
        cardcode = random.choice(codes)
    else:
        draft_list = []
        for arr in draft_data:
            for code in arr:
                draft_list.append(code)
        print(draft_list)
        for draft_card in draft_list:
            codes.remove(draft_card)
        cardcode = random.choice(codes)

    return cardcode


@drafts_tail.callback_query(F.data.startswith("draft_with_bot"))
async def draft_with_bot(callback: types.CallbackQuery, state: FSMContext):
    sqlite_connection = sqlite3.connect('tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()

    user_id = int(callback.from_user.id)
    username = callback.from_user.username
    picks = json.dumps([])
    bans = json.dumps([])
    # first_pick = random.choice([0, 1])
    first_pick = 0
    if first_pick == 1:
        nickname1 = '@' + username
        nickname2 = '@KKimpactBOT'
    else:
        nickname2 = '@' + username
        nickname1 = '@KKimpactBOT'
    filename = str(user_id)
    # photo = BufferedInputFile(photo, filename="file.txt")
    draft_data = [[], [], [], []]

    if first_pick == 0:
        draft_answer = await create_draft_answer('ВАШ БАН')
        photo = create_draft_tail_img(99, None, filename, nickname1, nickname2)
        cardcode = random_cardcode(draft_data=0)
        print(cardcode)
        photo = create_draft_tail_img(0, cardcode, str(user_id), resonance1=[],
                                      resonance2=[])
        # cardcode = random_cardcode(draft_data=[[cardcode], [], [], []])
        # print(cardcode)
        # photo = create_draft_tail_img(1, cardcode, str(user_id), resonance1=[],
        #                               resonance2=[])
        message_obj = await bot.send_photo(
            chat_id=user_id,
            caption=draft_answer,
            parse_mode=ParseMode.HTML,
            reply_markup=kb_draft_tail,
            photo=photo
        )
        draft_data[0].append(cardcode)
    else:
        photo = create_draft_tail_img(99, None, filename, nickname1, nickname2)
        draft_answer = await create_draft_answer('ВАШ БАН')
        message_obj = await bot.send_photo(
            chat_id=user_id,
            caption=draft_answer,
            parse_mode=ParseMode.HTML,
            reply_markup=kb_draft_tail,
            photo=photo
        )
    print(draft_data)
    message_id = message_obj.message_id
    cursor.execute(
        f"INSERT INTO main.draft_tail (user_id, message_id, first_pick, datatime, opponent, stage, draft_data)"
        f"VALUES (?, ?, ?, ?, ?, ?, ?)",
        (user_id, message_id, first_pick,
         int(datetime.now().timestamp()), 1, 0, json.dumps(draft_data))
    )
    sqlite_connection.commit()

    cursor.execute(
        f"UPDATE main.draft_tail_queue SET requested = NULL, in_the_queue = 0 "
        f"WHERE user_id = {user_id}"
    )
    sqlite_connection.commit()

    await state.set_state('DraftTailBOT')


@drafts_tail.message(F.sticker, StateFilter('DraftTailBOT'))
async def sticker_with_bot(message: types.Message, state: FSMContext):
    result: bool = await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    sticker_uid = message.sticker.file_unique_id

    sqlite_connection = sqlite3.connect('tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()

    cursor.execute(
        f"SELECT user_id, message_id, picks, bans, first_pick, opponent, stage, draft_data"
        f" FROM main.draft_tail WHERE user_id = '{message.from_user.id}'"
        f"ORDER BY id DESC"
    )
    r = cursor.fetchall()
    if len(r) != 0:
        r = r[0]
        user_id = r[0]
        message_id = r[1]
        picks = json.loads(r[2])
        bans = json.loads(r[3])
        first_pick = r[4]
        opponent = r[5]
        stage = r[6]
        draft_data = json.loads(r[7])
        card_code = await get_card_number_by_sticker(sticker_uid)
        if card_code == 0:
            await draft_error(error_text='ОШИБКА! Я не знаю такой стикер!', message=message)

        if stage == 0:
            # 1 бан I игрока
            if first_pick:
                # print('1 бан I игрока')
                if await add_new_card_to_drafts_data(card_code, 'bans', bans, user_id, draft_data):
                    await update_drafts(
                        user_id, opponent, fp_status='БАН ПРОТИВНИКА', scp_status='ВАШ БАН', stage=stage, cardcode=card_code)
                    await stage_update(1, user_id)
                    await stage_update(1, opponent)
                else:
                    # карта уже есть в драфтах
                    await draft_error(error_text='неизвестная ошибка, отправьте скриншот @maksenro', message=message)
            else:
                # ожидаем 1 бана I игрока
                await draft_error(error_text='ОШИБКА! Сейчас бан противника!', message=message)

        if stage == 1:
            # 1 бан II игрока
            if first_pick:
                # ожидаем 1 бана II игрока
                await draft_error(error_text='ОШИБКА! Сейчас бан противника!', message=message)
            else:
                # print('1 бан II игрока')
                if await add_new_card_to_drafts_data(card_code, 'bans', bans, user_id, draft_data):
                    await update_drafts(
                        opponent, user_id, fp_status='ПИК ПРОТИВНИКА', scp_status='ВАШ ПИК', stage=stage, cardcode=card_code)
                    await stage_update(2, user_id)
                    await stage_update(2, opponent)
                else:
                    # карта уже есть в драфтах
                    await draft_error(error_text='ОШИБКА! Повтор карты, проверьте пики и баны!', message=message)

        if stage == 2:
            # 1 пик II игрока
            if first_pick:
                # ожидаем 1 пик II игрока
                await draft_error(error_text='ОШИБКА! Сейчас пик противника!', message=message)
            else:
                # print('1 бан II игрока')
                if await add_new_card_to_drafts_data(card_code, 'picks', picks, user_id, draft_data):
                    await update_drafts(
                        opponent, user_id, fp_status='ВАШ БАН', scp_status='БАН ПРОТИВНИКА', stage=stage, cardcode=card_code)
                    await stage_update(3, user_id)
                    await stage_update(3, opponent)
                else:
                    # карта уже есть в драфтах
                    await draft_error(error_text='ОШИБКА! Повтор карты, проверьте пики и баны!', message=message)

        if stage == 3:
            # 2 бан I игрока
            if first_pick:
                if await add_new_card_to_drafts_data(card_code, 'bans', bans, user_id, draft_data):
                    await update_drafts(
                        user_id, opponent, fp_status='ВАШ ПИК', scp_status='ПИК ПРОТИВНИКА', stage=stage, cardcode=card_code)
                    await stage_update(4, user_id)
                    await stage_update(4, opponent)
                else:
                    # карта уже есть в драфтах
                    await draft_error(error_text='ОШИБКА! Повтор карты, проверьте пики и баны!', message=message)
            else:
                # ожидаем 2 бан I игрока
                await draft_error(error_text='ОШИБКА! Сейчас бан противника!', message=message)

        if stage == 4:
            # 1 пик I игрока
            if first_pick:
                if await add_new_card_to_drafts_data(card_code, 'picks', picks, user_id, draft_data):
                    await update_drafts(
                        user_id, opponent, fp_status='БАН ПРОТИВНИКА', scp_status='ВАШ БАН', stage=stage, cardcode=card_code)
                    await stage_update(5, user_id)
                    await stage_update(5, opponent)
                else:
                    # карта уже есть в драфтах
                    await draft_error(error_text='ОШИБКА! Повтор карты, проверьте пики и баны!', message=message)
            else:
                # ожидаем 1 пик I игрока
                await draft_error(error_text='ОШИБКА! Сейчас пик противника!', message=message)

        if stage == 5:
            # 2 бан II игрока
            if first_pick:
                # ожидаем 2 бана II игрока
                await draft_error(error_text='ОШИБКА! Сейчас бан противника!', message=message)
            else:
                if await add_new_card_to_drafts_data(card_code, 'bans', bans, user_id, draft_data):
                    await update_drafts(
                        opponent, user_id, fp_status='ПИК ПРОТИВНИКА', scp_status='ВАШ ПИК', stage=stage, cardcode=card_code)
                    await stage_update(6, user_id)
                    await stage_update(6, opponent)
                else:
                    # карта уже есть в драфтах
                    await draft_error(error_text='ОШИБКА! Повтор карты, проверьте пики и баны!', message=message)

        if stage == 6:
            # 2 пик II игрока
            if first_pick:
                # ожидаем 2 пик II игрока
                await draft_error(error_text='ОШИБКА! Сейчас пик противника!', message=message)
            else:
                if await add_new_card_to_drafts_data(card_code, 'picks', picks, user_id, draft_data):
                    await update_drafts(
                        opponent, user_id, fp_status='ВАШ ПИК', scp_status='ПИК ПРОТИВНИКА', stage=stage, cardcode=card_code)
                    await stage_update(7, user_id)
                    await stage_update(7, opponent)
                else:
                    # карта уже есть в драфтах
                    await draft_error(error_text='ОШИБКА! Повтор карты, проверьте пики и баны!', message=message)

        if stage == 7:
            # 2 пик I игрока
            if first_pick:
                if await add_new_card_to_drafts_data(card_code, 'picks', picks, user_id, draft_data):
                    await update_drafts(
                        user_id, opponent, fp_status='ВАШ ПИК', scp_status='ПИК ПРОТИВНИКА', stage=stage, cardcode=card_code)
                    await stage_update(8, user_id)
                    await stage_update(8, opponent)
                else:
                    # карта уже есть в драфтах
                    await draft_error(error_text='ОШИБКА! Повтор карты, проверьте пики и баны!', message=message)
            else:
                # ожидаем 2 пик I игрока
                await draft_error(error_text='ОШИБКА! Сейчас пик противника!', message=message)

        if stage == 8:
            # 3 пик I игрока
            if first_pick:
                if await add_new_card_to_drafts_data(card_code, 'picks', picks, user_id, draft_data):
                    await update_drafts(
                        user_id, opponent, fp_status='ПИК ПРОТИВНИКА', scp_status='ВАШ ПИК', stage=stage, cardcode=card_code)
                    await stage_update(9, user_id)
                    await stage_update(9, opponent)
                else:
                    # карта уже есть в драфтах
                    await draft_error(error_text='ОШИБКА! Повтор карты, проверьте пики и баны!', message=message)
            else:
                # ожидаем 3 пик I игрока
                await draft_error(error_text='ОШИБКА! Сейчас пик противника!', message=message)

        if stage == 9:
            # 3 пик II игрока
            if first_pick:
                # ожидаем 3 пик II игрока
                await draft_error(error_text='ОШИБКА! Сейчас пик противника!', message=message)
            else:
                if await add_new_card_to_drafts_data(card_code, 'picks', picks, user_id, draft_data):
                    draft_data = []
                    message_ids = []  # usr1, usr2
                    fp_status = 'КОНЕЦ ДРАФТОВ'
                    scp_status = 'КОНЕЦ ДРАФТОВ'
                    picks = []
                    users_ids = [user_id, opponent]
                    opponent_ids = [opponent, user_id]

                    for user_id in users_ids:
                        cursor.execute(
                            f"SELECT message_id, picks, bans FROM main.draft_tail WHERE user_id = {user_id} ORDER BY id DESC"
                        )
                        r = cursor.fetchall()
                        if len(r) == 0:
                            draft_data.append([])
                            draft_data.append([])
                        else:
                            r = r[0]
                            message_ids.append(r[0])
                            codes_picks = json.loads(r[1])
                            codes_bans = json.loads(r[2])
                            names_picks = []
                            names_bans = []
                            for code_pick in codes_picks:
                                names_picks.append(get_name_card_by_code(code_pick))
                            for code_ban in codes_bans:
                                names_bans.append(get_name_card_by_code(code_ban))

                            picks.append(codes_picks)
                            draft_data.append(names_picks)
                            draft_data.append(names_bans)

                    c = 0
                    resonances = []
                    for pick in picks:
                        resonances.append(find_resonance(pick))
                    photo = create_draft_tail_img(stage, card_code, users_ids[0] + users_ids[1], resonance1=resonances[1],
                                                  resonance2=resonances[0])

                    for status in [fp_status, scp_status]:
                        draft_answer = await create_draft_answer(status, draft_data)
                        media_photo = InputMediaPhoto(media=photo, caption=draft_answer, parse_mode=ParseMode.HTML)
                        message_obj = await bot.edit_message_media(
                            chat_id=users_ids[c],
                            message_id=message_ids[c],
                            reply_markup=kb_draft_tail_who_win(opponent_ids[c]),
                            media=media_photo
                        )
                        c += 1

                    cursor.execute(
                        f"INSERT INTO main.draft_tail_history (user_id, datatime, first_pick, opponent, draft_data) VALUES (?, ?, ?, ?, ?)", (users_ids[0], int(datetime.now().timestamp()), 0, users_ids[1], json.dumps(draft_data))
                    )
                    sqlite_connection.commit()
                    cursor.execute(
                        f"INSERT INTO main.draft_tail_history (user_id, datatime, first_pick, opponent, draft_data) VALUES (?, ?, ?, ?, ?)", (users_ids[1], int(datetime.now().timestamp()), 1, users_ids[0], json.dumps(draft_data))
                    )
                    sqlite_connection.commit()
                    cursor.execute(
                        f"DELETE FROM main.draft_tail WHERE user_id = {users_ids[0]} OR user_id = {users_ids[1]}"
                    )
                    sqlite_connection.commit()

                else:
                    # карта уже есть в драфтах
                    await draft_error(error_text='ОШИБКА! Повтор карты, проверьте пики и баны!', message=message)

        if stage == 10:
            print('Последний пик противника')

    else:
        await message.answer(
            text='Ваши драфты удалены тк прошло больше 24ч с момента их начала', reply_markup=kb_ru_main
        )




#
#
# @drafts_tail.message(DraftTail.your_pick, F.sticker)
# async def get_pick(message: types.Message, state: FSMContext):
#     sticker_uid = message.sticker.file_unique_id
#     result: bool = await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
#     sqlite_connection = sqlite3.connect('tcgCodes.sqlite')
#     cursor = sqlite_connection.cursor()
#     cursor.execute(f"SELECT card_name_ru FROM main.role_cards WHERE sticker_uid = '{sticker_uid}'")
#     r = cursor.fetchall()
#     if len(r) == 0:
#         pass
#     else:
#         card_name = r[0][0]
#         cursor.close()
#
#         state_data = await state.get_data()
#         state_data['your_picks'].append(card_name)
#
#         await state.update_data(your_picks=state_data['your_picks'])
#
#         state_data = await state.get_data()
#         draft_answer = create_draft_answer(state_data)
#
#         await bot.edit_message_text(
#             text=draft_answer, chat_id=message.chat.id,
#             message_id=state_data['drafts_message_id'],
#             parse_mode=ParseMode.HTML,
#             disable_web_page_preview=True
#         )
# print(state_data)
# state_data = await state.get_data()

# await message.answer(str(state_data))
# await state.update_data(drafts_message_id=card_name)


# @drafts_tail.message(DraftTail.your_ban, F.sticker)
# async def get_ban(message: types.Message, state: FSMContext):
#
#
# @drafts_tail.message(DraftTail.enemy_pick, F.sticker)
# async def wait_pick(message: types.Message, state: FSMContext):
#
#
# @drafts_tail.message(DraftTail.enemy_ban, F.sticker)
# async def wait_ban(message: types.Message, state: FSMContext):
#
