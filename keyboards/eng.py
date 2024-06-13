from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb_main_eng = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🦊 Драфты Хвост")],
        [KeyboardButton(text="Generate deck"), KeyboardButton(text="from Hoyolab")],
        [KeyboardButton(text="Generate 2"), KeyboardButton(text="2 from Hoyolab")],
        [KeyboardButton(text="Generate 10"), KeyboardButton(text="10 from Hoyolab")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Which deck do you want?"
)
