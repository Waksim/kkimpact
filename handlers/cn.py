import sqlite3
from datetime import datetime

from aiogram.enums import ParseMode
from aiogram.utils.media_group import MediaGroupBuilder
from loguru import logger

from aiogram import types, Router, F, Bot, html

from functions import random_hoyolab, generate_deck
from functions.create_image import create_decks_img
from keyboards.cn import kb_main_cn

# logger.add('telegram_bot.log', level='DEBUG', format="{time:MMM-DD – HH:mm:ss} – {message}", rotation="100 MB",
#            enqueue=True)
bot = Bot(token="<TOKEN_TEST>")   # TEST
# bot = Bot(token="<TOKEN_MAIN>")   # MAIN
cn = Router()


# ____________________________________________________________________


@cn.message(F.text.lower() == "🇨🇳 中文")
async def cmd_start(message: types.Message):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    sqlite_connection = sqlite3.connect('tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()
    cursor.execute("UPDATE telegram_users SET preferens = 'cn' WHERE tg_id = ?;", (message.from_user.id,))
    sqlite_connection.commit()
    cursor.close()

    await message.answer_sticker('CAACAgIAAxkBAAELtbNl9Hx92wKQloh3xmrWEiu5Pui-nwACTU4AAmhnoEue0q81egR3KTQE')
    await message.answer("嗨!\n" +
                         "1) 我可以创建随机卡片组，或者从Hoyolab中获取它们。\n" +
                         "甲板代码是可点击的,点击他们 " + html.code("复制") + " (←可点击).\n" +
                         "2）您可以一次给我发送最多10个甲板代码，我会解密它们并向您发送照片和构图。\n\n" +
                         "发送 /start 或 /choose_lang - 如果你想改变语言\n"
                         , reply_markup=kb_main_cn, parse_mode=ParseMode.HTML)


@cn.message(F.text.lower() == "生成随机甲板")  # 🇨🇳
async def cmd_start(message: types.Message):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    generated_deck = generate_deck.get_random_code(card_name_lang='card_name_cn')
    deck_code = generated_deck[0]
    deck_role_cards = generated_deck[1]

    answer_text = (f"{html.bold(html.quote(deck_role_cards))}\n" +
                   html.code(html.quote(deck_code)))
    photo = create_decks_img(deck_code=deck_code)
    await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=answer_text, parse_mode=ParseMode.HTML,
                         reply_markup=kb_main_cn)


@cn.message(F.text.lower() == "甲板与hoyolab")  # 🇨🇳
async def cmd_start(message: types.Message):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    deck_data = random_hoyolab.get_random_code_from_hoyolab(table_lang='hoyolab_decks_cn')

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
            html.bold(html.quote("🃏 扑克牌:  ")) + f"{role_card_names}\n\n" +
            html.bold(html.quote("🏷️ 标题:  ")) + f"{deck_title}\n\n" +
            html.bold(html.quote(
                "👤 标题:  ")) + f"{author_nickname}, uid - {html.code(html.quote(author_uid))} ({server}) \n\n" +
            html.bold(html.quote("🕗 创建日期:  ")) + f"{creation_time}\n\n" +
            html.bold(html.quote("📝 资料描述:  ")) + f"{description}\n\n" +
            html.bold(html.quote("#️⃣ 密码:  ")) + html.code(html.quote(deck_code)))

    photo = create_decks_img(role_cards=role_cards_codes, action_cards=action_cards_codes)

    caption_len = len(answer_text)
    print(caption_len)
    # 1024 предел
    if caption_len < 1000:
        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=answer_text, parse_mode=ParseMode.HTML,
                             reply_markup=kb_main_cn)
    else:
        await bot.send_photo(chat_id=message.chat.id, photo=photo, parse_mode=ParseMode.HTML)
        await message.answer(answer_text, parse_mode=ParseMode.HTML, reply_markup=kb_main_cn)


@cn.message(F.text.regexp(r"^生成(\d+)$").as_("digits"))  # 🇨🇳
async def cmd_start(message: types.Message, digits: list[str]):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    album_builder = MediaGroupBuilder()
    caption_text = ''
    counter = int(digits[1]) + 1

    for i in range(1, counter):
        generated_deck = generate_deck.get_random_code(card_name_lang='card_name_cn')
        deck_code = generated_deck[0]
        deck_role_cards = generated_deck[1]

        caption_text += (f"{i}) {html.bold(html.quote(deck_role_cards))}\n" +
                         html.code(html.quote(deck_code)) + "\n")
        photo = create_decks_img(deck_code=deck_code)

        album_builder.add_photo(media=photo, parse_mode=ParseMode.HTML)

    if len(caption_text) < 1000:
        album_builder.caption = caption_text
        await message.answer_media_group(media=album_builder.build(), reply_markup=kb_main_cn)
    else:
        await message.answer_media_group(media=album_builder.build())
        await message.answer(caption_text, parse_mode=ParseMode.HTML, reply_markup=kb_main_cn)


@cn.message(F.text.regexp(r"^(\d+) Hoyolab$").as_("digits"))  # 🇨🇳
async def cmd_start(message: types.Message, digits: list[str]):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    album_builder = MediaGroupBuilder()
    caption_text = ''
    counter = int(digits[1]) + 1

    for i in range(1, counter):
        deck_data = random_hoyolab.get_random_code_from_hoyolab(table_lang='hoyolab_decks_cn')

        role_card_names = deck_data[1]
        deck_code = deck_data[2]

        caption_text += (f"{i}) {html.bold(html.quote(role_card_names))}\n" +
                         html.code(html.quote(deck_code)) + "\n")
        photo = create_decks_img(deck_code=deck_code)

        album_builder.add_photo(media=photo, parse_mode=ParseMode.HTML)

    if len(caption_text) < 1000:
        album_builder.caption = caption_text
        await message.answer_media_group(media=album_builder.build(), reply_markup=kb_main_cn)
    else:
        await message.answer_media_group(media=album_builder.build())
        await message.answer(caption_text, parse_mode=ParseMode.HTML, reply_markup=kb_main_cn)
