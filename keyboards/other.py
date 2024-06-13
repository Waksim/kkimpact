from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇺🇸 English")],
        [KeyboardButton(text="🇺🇦 Український"), KeyboardButton(text="🇨🇳 中文")],
    ],
    resize_keyboard=True,
    input_field_placeholder="????"
)
