from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

kb_main_cn = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="生成随机甲板"), KeyboardButton(text="甲板与Hoyolab")],
        [KeyboardButton(text="生成2"), KeyboardButton(text="2 Hoyolab")],
        [KeyboardButton(text="生成10"), KeyboardButton(text="10 Hoyolab")],
        [KeyboardButton(text="🦊 Драфты Хвост"), KeyboardButton(text="😼 漏-草稿", web_app=WebAppInfo(url=f'https://invokationakademy.github.io/gitcg-draft/'))]
    ],
    resize_keyboard=True,
    input_field_placeholder="你想要哪套甲板?"
)
