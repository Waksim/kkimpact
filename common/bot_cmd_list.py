from aiogram.types import BotCommand


private_menu = [
    BotCommand(command='choose_lang', description='Change language'),
    BotCommand(command='menu', description='Main menu'),
]

admin_menu = [
    BotCommand(command='choose_lang', description='Change language'),
    BotCommand(command='menu', description='Main menu'),
    BotCommand(command='stat', description='Statistics'),
]