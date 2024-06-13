from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_stat_admin = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/100_mess_stat")],
        [KeyboardButton(text="/10_mess_stat")],
        [KeyboardButton(text="/last_5_usr")],
        [KeyboardButton(text="/last_50_usr")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Admin menu:"
)
