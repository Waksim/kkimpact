from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

kb_main_eng = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Generate deck"), KeyboardButton(text="from Hoyolab")],
        [KeyboardButton(text="Generate 2"), KeyboardButton(text="2 from Hoyolab")],
        [KeyboardButton(text="Generate 10"), KeyboardButton(text="10 from Hoyolab")],
        [KeyboardButton(text="🦊 Драфты Хвост"), KeyboardButton(text="😼 Blep-Drafts", web_app=WebAppInfo(url=f'https://invokationakademy.github.io/gitcg-draft/'))]
    ],
    resize_keyboard=True,
    input_field_placeholder="Which deck do you want?"
)
