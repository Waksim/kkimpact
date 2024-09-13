import asyncio  # Асинхронное программирование
import logging  # Логирование
import sqlite3  # Работа с SQLite
from typing import Any, Callable, Dict, Awaitable  # Аннотации типов

from aiogram import Bot, Dispatcher, types, BaseMiddleware, html, F  # Основные компоненты aiogram
from aiogram.dispatcher.flags import get_flag  # Работа с флагами
from aiogram.enums import ParseMode  # Режимы парсинга
from aiogram.filters.command import Command  # Командные фильтры
from aiogram.types import Message  # Сообщения
from aiogram.utils.chat_action import ChatActionSender  # Уведомления о действиях в чате
from aiogram.utils.i18n import I18n, ConstI18nMiddleware  # Интернационализация
from loguru import logger  # Логирование с помощью loguru

from config import settings  # Конфигурационные настройки
from common.bot_cmd_list import private_menu  # Команды бота
from filters.chat_type import ChatTypeFilter  # Фильтры по типу чата

# Импорты хендлеров
from handlers.admin import admin  # Административные функции
from handlers.blep_drafts import blep_drafts  # Черновики для Blep
from handlers.cn import cn  # Обработка сообщений на китайском
from handlers.drafts_tail import drafts_tail  # Черновики с хвостами
from handlers.eng import eng  # Обработка сообщений на английском
from handlers.group import group  # Обработка групповых сообщений
from handlers.others import others  # Обработка прочих сообщений
from handlers.ru import ru  # Обработка сообщений на русском
from handlers.ua import ua  # Обработка сообщений на украинском
from handlers.web_app import web_app  # Веб-приложение

# Импорты клавиатур
from keyboards.cn import kb_main_cn  # Основная клавиатура на китайском
from keyboards.eng import kb_main_eng  # Основная клавиатура на английском
from keyboards.other import start_kb  # Клавиатура для старта
from keyboards.ru import kb_ru_main  # Основная клавиатура на русском
from keyboards.ua import kb_main_ua  # Основная клавиатура на украинском


logging.basicConfig(level=logging.INFO)
logger.add('./telegram_bot.log', level='DEBUG', format="{time:MMM-DD – HH:mm:ss} – {message}", rotation="100 MB",
           enqueue=True)
logger.info("---START_BOT---")

bot = Bot(token=settings.bot_token)     # settings.toml

dp = Dispatcher()
dp.include_routers(group, web_app, ru, eng, ua, cn, drafts_tail, blep_drafts, admin, others)
# dp.include_routers(group, others, ru, eng, ua, cn, drafts_tail, admin)


class ChatActionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        long_operation_type = get_flag(data, "long_operation")

        # Если такого флага на хэндлере нет
        if not long_operation_type:
            return await handler(event, data)

        # Если флаг есть
        async with ChatActionSender(
                action=long_operation_type,
                chat_id=event.chat.id
        ):
            return await handler(event, data)


# ПОЛУЧЕНИЕ ID ИЗОБРАЖЕНИЯ
# @dp.message(F.photo)
# async def scan_message(msg: types.Message):
#     document_id = msg.photo[0].file_id
#     file_info = await bot.get_file(document_id)
#     print(f'file_id: {file_info.file_id}')
#     print(f'file_path: {file_info.file_path}')
#     print(f'file_size: {file_info.file_size}')
#     print(f'file_unique_id: {file_info.file_unique_id}')

@dp.message(ChatTypeFilter(chat_type=["private"]),
            Command("start", "choose_lang"))
async def cmd_start(message: types.Message):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    logger.info(f"@{message.from_user.username} – '{message.text}'")

    sqlite_connection = sqlite3.connect('./users_info.sqlite')
    cursor = sqlite_connection.cursor()

    tg_id = message.from_user.id

    cursor.execute("SELECT EXISTS(SELECT * FROM telegram_users where tg_id = ?)", (tg_id,))
    registered = cursor.fetchall()[0][0]

    if registered == 0:
        cursor.execute("""INSERT INTO telegram_users 
                (tg_id, nickname, username, tg_lang, premium) VALUES 
                (?, ?, ?, ?, ?);""",
                       (message.from_user.id, message.from_user.first_name,
                        message.from_user.username, message.from_user.language_code,
                        message.from_user.is_premium))
        sqlite_connection.commit()

    cursor.close()

    await message.answer_sticker('CAACAgIAAxkBAAELtIdl9D6luOGl3Mk7Kmy2BPeS7MotGgACyEMAAgfboUudKCeCJzz2OjQE')
    await message.answer("Привет? Hello? Привіт? 嗨？", reply_markup=start_kb)


# ____________________________________________________________________

@ru.message(ChatTypeFilter(chat_type=["private"]),
            Command("menu"))
async def menu(message: types.Message):
    user_id = message.from_user.id

    sqlite_connection = sqlite3.connect('./users_info.sqlite')
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


async def main():
    await bot.set_my_commands(commands=private_menu, scope=types.BotCommandScopeAllPrivateChats())

    i18n = I18n(path="locales", default_locale="ru", domain="kkimpact_bot")
    dp.message.outer_middleware(ConstI18nMiddleware(locale='ru', i18n=i18n))

    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
