import sqlite3

import requests


def decrypt_code(code):

    payload = '"code": "'+str(code)+'"'.format()
    url = 'https://sg-public-api.hoyolab.com/event/cardsquare/decode_card_code?lang=en-us'
    payload = '{'+payload+'}'
    r = requests.post(url, data=payload).json()

    if r['data'] is None:
        return [], []

    role_cards_arr = r['data']['role_cards']
    role_cards_ids = []
    action_cards_arr = r['data']['action_cards']
    action_cards_ids = []

    for role_card in role_cards_arr:
        role_cards_ids.append(role_card['basic']['item_id'])

    for action_card in action_cards_arr:
        action_cards_ids.append(action_card['basic']['item_id'])

    return role_cards_ids, action_cards_ids


def card_codes_to_deck_code(role_card_codes, action_card_codes):
    payload = '"action_cards":' + str(action_card_codes) + ',"role_cards":' + str(role_card_codes) + ''.format()
    # print(payload)
    url = 'https://sg-public-api.hoyolab.com/event/cardsquare/encode_card_code?lang=en-us'
    payload = '{' + payload + '}'
    r = requests.post(url, data=payload).json()

    deck_code = r["data"]["code"]

    return deck_code


def get_card_name_by_card_code(card_codes_arr):
    print(card_codes_arr)
    card_names = []

    sqlite_connection = sqlite3.connect('./tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()
    cursor.execute(f"SELECT code, card_name_ru FROM main.role_cards")
    role_cards = cursor.fetchall()
    cursor.execute(f"SELECT code, card_name_ru FROM main.action_cards")
    action_cards = cursor.fetchall()

    for card_code in card_codes_arr:
        for card_info in role_cards + action_cards:
            if int(card_info[0]) == int(card_code):
                card_names.append(str(card_info[1]))

    card_names_str = ""

    print(card_names)
    for card_name in card_names:
        card_names_str += card_name + ', '

    card_names_str = card_names_str[:-2]

    return card_names_str


# print(decrypt_code('AWDQ5hoPAhDw8VkPCiCw8rQPCzBQ9LUPC0Bg9bgPDGAg9sMPDHCA/MsQDqFQC+UQDrAA'))