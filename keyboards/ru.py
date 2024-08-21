from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
# 👥 🤖 🌐 🦊
kb_ru_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Сгенерировать деку"), KeyboardButton(text="Дека с Hoyolab")],
        # [KeyboardButton(text="Сгенерировать 2"), KeyboardButton(text="2 с Hoyolab")],
        # [KeyboardButton(text="Сгенерировать 10"), KeyboardButton(text="10 с Hoyolab")],
        # [KeyboardButton(text="🦊 Драфты Хвост"), KeyboardButton(text="Дек_билдер", web_app=WebAppInfo(url=f'https://waksim.github.io/blep-drafts/'))]
        [KeyboardButton(text="🦊 Драфты Хвост"), KeyboardButton(text="😼 Блеп-Драфты")],
        [KeyboardButton(text="😼 Блеп-СОЛО", web_app=WebAppInfo(url=f'https://waksim.github.io/blep-drafts/'))]
    ],
    resize_keyboard=True,
    row_width=100,
    input_field_placeholder="Какую деку хочешь?"
)


def kb_draft_queue(users_data, requested_user_id, blep=0):
    if blep:
        mode = 'b_'
    else:
        mode = ''

    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text="<-- Назад", callback_data="b_go_to_main_menu"))
    builder.add(InlineKeyboardButton(text="Обновить", callback_data=f"{mode}update_queue_list"))

    builder.add(InlineKeyboardButton(text="↓ Выберите оппонента ↓", callback_data="choose_opponent_alert"))

    c = 1
    for user in users_data:
        # user_id, message_id, username, firstname
        user_id = user[0]
        if user_id == requested_user_id:
            continue
        firstname = user[3]
        # for i in range(1, 21):
        builder.button(text=f"{c}) {firstname}", callback_data=f"b_draft_tail_request={user_id}")
        c += 1
    if len(users_data) > 30:
        builder.adjust(2, 1, 2)
    else:
        builder.adjust(2, 1)

    return builder.as_markup()


def kb_draft_tail_accept_decline(user_id, username, blep=0):
    if blep:
        mode = 'b_'
    else:
        mode = ''
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Принять", callback_data=f"{mode}draft_tail_accepted={user_id}={username}"),
                InlineKeyboardButton(text="❌ Отклонить", callback_data=f"{mode}draft_tail_declined={user_id}")
            ]
        ]
    )


def kb_draft_tail_who_win(user_id, blep=0):
    if blep:
        mode = 'b_'
    else:
        mode = ''
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔄 Повторить драфты", callback_data=f"{mode}draft_tail_request={user_id}"),
                InlineKeyboardButton(text="⬅️ В главное меню", callback_data=f"b_go_to_main_menu")
            ]
        ]
    )


kb_draft_tail = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="❄️ КРИО", url='https://t.me/addstickers/crio_by_KKImpact_testBOT'),
                InlineKeyboardButton(text="🌀 ГИДРО", url='https://t.me/addstickers/hydro_by_KKImpact_testBOT')
            ],
            [
                InlineKeyboardButton(text="🔥 ПИРО", url='https://t.me/addstickers/pyro_by_KKImpact_testBOT'),
                InlineKeyboardButton(text="⚡ ЭЛЕКТРО", url='https://t.me/addstickers/electro_by_KKImpact_testBOT')
            ],
            [
                InlineKeyboardButton(text="🍃 АНЕМО", url='https://t.me/addstickers/anemo_by_KKImpact_testBOT'),
                InlineKeyboardButton(text="🌕 ГЕО", url='https://t.me/addstickers/geo_by_KKImpact_testBOT')
            ],
            [
                InlineKeyboardButton(text="🍀 ДЕНДРО", url='https://t.me/addstickers/dendro_by_KKImpact_testBOT'),
                InlineKeyboardButton(text="ПРАВИЛА", callback_data=f"draft_tail_rules")
            ]
        ]
    )


def kb_start_blep_drafts(your_id, opp_id):

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="😼 Начать Драфты", web_app=WebAppInfo(url=f'https://waksim.github.io/blep-drafts/?your_id={your_id}&opp_id={opp_id}'))]
        ],
        # resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Начать драфты!"
    )