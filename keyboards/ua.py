from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

kb_main_ua = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Згенерувати деку"), KeyboardButton(text="Дека з Hoyolab")],
        [KeyboardButton(text="Згенерувати 2"), KeyboardButton(text="2 з Hoyolab")],
        [KeyboardButton(text="Згенерувати 10"), KeyboardButton(text="10 з Hoyolab")],
        # [KeyboardButton(text="🦊 Драфты Хвост"), KeyboardButton(text="Дек_билдер", web_app=WebAppInfo(url=f'https://waksim.github.io/kkimpact_web/'))]
        [KeyboardButton(text="🦊 Драфты Хвост"), KeyboardButton(text="😼 Блеп-Драфти", web_app=WebAppInfo(url=f'https://invokationakademy.github.io/gitcg-draft/'))]
    ],
    resize_keyboard=True,
    input_field_placeholder="Яку деку хочеш?"
)
