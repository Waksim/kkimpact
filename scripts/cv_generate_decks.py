import sqlite3

import requests

sqlite_connection = sqlite3.connect('../tcgCodes.sqlite')
cursor = sqlite_connection.cursor()

cursor.execute(f"SELECT code FROM main.cv_weights WHERE link_with_char != 0")
r = cursor.fetchall()

cards_arr = []
action_cards_CODEs = []
role_cards_CODEs = []

for a in r:
    action_card = a[0]
    if len(action_cards_CODEs) < 30:
        action_cards_CODEs.append(action_card)
    if len(action_cards_CODEs) == 30:
        payload = '"action_cards":'+str(action_cards_CODEs)+',"role_cards":'+str(role_cards_CODEs)+''.format()
        # print(payload)
        url = 'https://sg-public-api.hoyolab.com/event/cardsquare/encode_card_code?lang=en-us'
        payload = '{'+payload+'}'
        r = requests.post(url, data=payload).json()

        deck_code = r["data"]["code"]

        print(deck_code)
        action_cards_CODEs = []