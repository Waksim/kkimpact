import sqlite3

from aiogram import Router, Bot, types
from aiogram.filters.command import Command

from keyboards.admin import kb_stat_admin
from config import settings


bot = Bot(token=settings.bot_token)   # TEST
# bot = Bot(token="<TOKEN_MAIN>")   # MAIN
admin = Router()


@admin.message(Command("100_mess_stat", "10_mess_stat", "last_5_usr", "last_50_usr"))
async def cmd_start(message: types.Message):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    # logger.info(f"@{message.from_user.username} – '{message.text}'")

    sqlite_connection = sqlite3.connect('tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()

    last_log = 0
    last_usr = 0

    if message.text == '/10_mess_stat':
        last_log = 10
    if message.text == '/100_mess_stat':
        last_log = 100
    if message.text == '/last_5_usr':
        last_usr = 5
    if message.text == '/last_50_usr':
        last_usr = 50

    if last_log != 0:
        if message.from_user.id in [382202500, 799890260]:
            answer_string = ''
            with open('telegram_bot.log') as file:
                for line in (file.readlines()[-last_log:]):
                    answer_string += line + '\n'

            await message.answer(f"Последние {last_log} сообщений боту:\n\n" + answer_string[-4000:])

    if last_usr != 0:
        if message.from_user.id in [382202500, 799890260]:
            cursor.execute(f"SELECT * FROM telegram_users ORDER BY id desc LIMIT {last_usr}")
            registered_users = cursor.fetchall()
            registered_users.reverse()
            cursor.close()

            last_5_users = ''

            for registered_user in registered_users:
                last_5_users += str(registered_user[0]) + ', '
                # last_5_users += str(registered_user[1]) + ', '
                last_5_users += str(registered_user[2]) + ', '
                last_5_users += '@' + str(registered_user[3]) + ', '
                last_5_users += str(registered_user[4]) + ', '
                last_5_users += str(registered_user[5]) + ', '
                last_5_users += str(registered_user[6]) + '\n'

            print(last_5_users)
            await message.answer(f"Последние зарегестрированные:\n\n" + last_5_users)


@admin.message(Command("stat"))
async def cmd_start(message: types.Message):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    await message.answer(f"Меню администратора:", reply_markup=kb_stat_admin)
