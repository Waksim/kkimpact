import requests
import sqlite3
import random


def get_random_code(card_name_lang):
    sqlite_connection = sqlite3.connect('./tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()

    cursor.execute(f"SELECT id, code, element, {card_name_lang} FROM main.role_cards")
    role_cards = cursor.fetchall()

    rands = random.sample(role_cards, k=3)
    role_cards_IDs = []
    role_cards_CODEs = []
    role_cards_ELEM = []
    role_cards_NAMEs = ''
    action_cards_CODEs = []

    for rand in rands:
        role_cards_IDs.append(rand[0])
        role_cards_CODEs.append(rand[1])
        role_cards_NAMEs += rand[3] + ', '

        role_cards_ELEM_list = str(rand[2]).split(", ")
        for i in role_cards_ELEM_list:
            role_cards_ELEM.append(i)

    duplicate_elements = []
    resonance = []

    for i in role_cards_ELEM:
        if i in duplicate_elements:
            resonance.append(i)
        else:
            duplicate_elements.append(i)

    resonance.append('0')
    resonance.append('0')
    resonance.append('0')
    resonance.append('0')

    cursor.execute('SELECT code FROM main.action_cards_2x WHERE (link_with_char = 0 OR link_with_char = ? OR link_with_char = ? OR link_with_char = ?) AND (resonance = 0 OR resonance = ? OR resonance = ? OR resonance = ? OR resonance = ?)', (role_cards_IDs[0], role_cards_IDs[1], role_cards_IDs[2], resonance[0], resonance[1], resonance[2], resonance[3]))
    action_cards = cursor.fetchall()
    cursor.close()


    rands = random.sample(action_cards, k=30)
    for rand in rands:
        action_cards_CODEs.append(rand[0])

    # for role_card in role_cards:
    #     role_card_ID = role_card[0]
    #     # role_card_NAME = role_card[1]
    #     role_card_CODE = role_card[1]

    payload = '"action_cards":'+str(action_cards_CODEs)+',"role_cards":'+str(role_cards_CODEs)+''.format()
    # print(payload)
    url = 'https://sg-public-api.hoyolab.com/event/cardsquare/encode_card_code?lang=en-us'
    payload = '{'+payload+'}'
    r = requests.post(url, data=payload).json()

    deck_code = r["data"]["code"]
    role_cards_NAMEs = role_cards_NAMEs[:-2]
    for_return = [deck_code, role_cards_NAMEs]

    # print(for_return)

    return for_return


# r = get_random_code(card_name_lang='card_name_ru')
# print(r)
# get_random_code(card_name_lang='card_name_ua')
# get_random_code(card_name_lang='card_name_cn')
# get_random_code(card_name_lang='card_name_eng')


# payload = '"action_cards":[322012, 332021, 311206, 311105, 322002, 217011, 311403, 321016, 312021, 312501, 331701, 333008, 311203, 322012, 312010, 312004, 332009, 311101, 312001, 311202, 332018, 333007, 332002, 323006, 321015, 333005, 312015, 333009, 322023, 323004],"role_cards":[1701, 1704, 1110]'
# # ['AtDwnTIJFHDg+c0HEJBQlIMHB/HQAsMQBvCw8osTE5BRwTMQCtDQousREREASoANDJAA', 'Коллеи, Яо Яо, Шарлотта']
# # print(payload)
# url = 'https://sg-public-api.hoyolab.com/event/cardsquare/encode_card_code?lang=en-us'
# payload = '{'+payload+'}'
# r = requests.post(url, data=payload).json()
# deck_code = r["data"]["code"]
# print(deck_code)


