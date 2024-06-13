from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_main_ua = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🦊 Драфты Хвост")],
        [KeyboardButton(text="Згенерувати деку"), KeyboardButton(text="Дека з Hoyolab")],
        [KeyboardButton(text="Згенерувати 2"), KeyboardButton(text="2 з Hoyolab")],
        [KeyboardButton(text="Згенерувати 10"), KeyboardButton(text="10 з Hoyolab")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Яку деку хочеш?"
)
