# 1. Стандартные библиотеки
import sqlite3
from datetime import datetime

# 2. Библиотеки сторонних разработчиков
from aiogram import Bot, Dispatcher, types, Router, F, html
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.utils.media_group import MediaGroupBuilder
from loguru import logger

# 3. Локальные модули
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
    # Уведомляем пользователя о начале обработки запроса
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    # Обновление предпочтений пользователя в базе данных
    with sqlite3.connect('./users_info.sqlite') as sqlite_connection:
        cursor = sqlite_connection.cursor()
        cursor.execute(
            "UPDATE telegram_users SET preferens = 'ru' WHERE tg_id = ?;",
            (message.from_user.id,)
        )
        sqlite_connection.commit()

    # Отправка стикера и сообщения
    sticker_id = 'CAACAgIAAxkBAAELtbNl9Hx92wKQloh3xmrWEiu5Pui-nwACTU4AAmhnoEue0q81egR3KTQE'
    welcome_message = _(
        "Привет, Картоботик!\n"
        "1) Я могу создавать рандомные деки, либо брать их с Hoyolab.\n"
        "Коды колод кликабельны, нажми на них, чтобы " + html.code("СКОПИРОВАТЬ") + " (←кликабельно).\n"
        "2) Можешь отправить мне до 10 кодов-колод за раз, я их расшифрую и пришлю тебе фото и состав.\n\n"
        "Отправь /start или /choose_lang, если хочешь поменять язык\n"
    )

    await message.answer_sticker(sticker_id)
    await message.answer(
        welcome_message,
        reply_markup=kb_ru_main,
        parse_mode=ParseMode.HTML
    )


@ru.message(F.text == "💰 Поддержать")
async def donations(message: types.Message):
    # Уведомляем пользователя о начале обработки запроса
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    # Отправка стикера и сообщения
    welcome_message = _(
        html.bold("Поддержать бота:\n\n")
        + "https://www.donationalerts.com/c/kkimpact\n\n"
        "Ваша поддержка значительно ускорит разработку бота.\n\n"
        "Спасибо за поддержку:\n\n"
        "..."
    )
    keyboard = [
        [InlineKeyboardButton(text="<-- Назад", callback_data="b_go_to_main_menu")]
    ]

    await message.answer_photo(
        photo='AgACAgIAAxkBAAIfIWbOKjuwRezCqkLQ1VmUR89G5RqrAAL55DEbNCpwSp8bguA75E90AQADAgADcwADNQQ',
        caption=welcome_message,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
    )

# ____________________________________________________________________
@ru.message(F.text.lower() == "сгенерировать деку", flags={"long_operation": "typing"})  # 🇷🇺
async def cmd_start(message: types.Message):
    # Уведомляем о начале обработки запроса
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    # Генерация случайного набора карт
    generated_deck = generate_deck.get_random_code(card_name_lang='card_name_ru')
    deck_code, deck_role_cards = generated_deck

    # Формирование текста ответа
    answer_text = (
        f"{html.bold(html.quote(deck_role_cards))}\n"
        f"{html.code(html.quote(deck_code))}"
    )

    # Создание изображения для дек
    photo = create_decks_img(deck_code=deck_code)

    # Отправка фотографии с подписью
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=photo,
        caption=answer_text,
        parse_mode=ParseMode.HTML,
        reply_markup=kb_ru_main
    )


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

    answer_text = _(
        html.bold(html.quote(_("🃏 Карты:  "))) + f"{role_card_names}\n\n" +
        html.bold(html.quote(_("🏷️ Название:  "))) + f"{deck_title}\n\n" +
        html.bold(html.quote(
            _("👤 Автор:  "))) + f"{author_nickname}, uid - {html.code(html.quote(author_uid))} ({server}) \n\n" +
        html.bold(html.quote(_("🕗 Дата создания:  "))) + f"{creation_time}\n\n" +
        html.bold(html.quote(_("📝 Описание:  "))) + f"{description}\n\n" +
        html.bold(html.quote(_("#️⃣ Код:  "))) + html.code(html.quote(deck_code))
    )

    photo = create_decks_img(role_cards=role_cards_codes, action_cards=action_cards_codes)

    caption_len = len(answer_text)
    # print(caption_len)
    # 1024 предел
    if caption_len < 1000:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption=answer_text,
            parse_mode=ParseMode.HTML,
            reply_markup=kb_ru_main
        )
    else:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            parse_mode=ParseMode.HTML
        )
        await message.answer(
            answer_text,
            parse_mode=ParseMode.HTML,
            reply_markup=kb_ru_main
        )


@ru.message(F.text.regexp(r"^Сгенерировать (\d+)$").as_("digits"), flags={"long_operation": "typing"})  # 🇷🇺
async def cmd_start(message: types.Message, digits: list[str]):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    album_builder = MediaGroupBuilder()
    caption_text = ''
    num_decks = int(digits[1]) + 1

    for i in range(1, num_decks):
        generated_deck = generate_deck.get_random_code(card_name_lang='card_name_ru')
        deck_code = generated_deck[0]
        deck_role_cards = generated_deck[1]

        # Формируем текст для подписи
        caption_text += (
            f"{i}) {html.bold(html.quote(deck_role_cards))}\n"
            f"{html.code(html.quote(deck_code))}\n"
        )

        # Создаем фото дек
        photo = create_decks_img(deck_code=deck_code)
        album_builder.add_photo(media=photo, parse_mode=ParseMode.HTML)

    # Проверяем длину текста для подписи и отправляем ответ
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
    num_decks = int(digits[1]) + 1

    for i in range(1, num_decks):
        deck_data = random_hoyolab.get_random_code_from_hoyolab(table_lang='hoyolab_decks_ru')
        role_card_names = deck_data[1]
        deck_code = deck_data[2]

        # Формирование текста для подписи
        caption_text += (
            f"{i}) {html.bold(html.quote(role_card_names))}\n"
            f"{html.code(html.quote(deck_code))}\n"
        )

        # Создание фото дек
        photo = create_decks_img(deck_code=deck_code)
        album_builder.add_photo(media=photo, parse_mode=ParseMode.HTML)

    # Отправка медиагруппы с текстом в зависимости от длины подписи
    if len(caption_text) < 1000:
        album_builder.caption = caption_text
        await message.answer_media_group(
            media=album_builder.build(),
            reply_markup=kb_ru_main
        )
    else:
        await message.answer_media_group(media=album_builder.build())
        await message.answer(
            caption_text,
            parse_mode=ParseMode.HTML,
            reply_markup=kb_ru_main
        )
