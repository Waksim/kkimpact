import requests
import sqlite3
import time


sqlite_connection = sqlite3.connect('./tcgCodes.sqlite')
cursor = sqlite_connection.cursor()

def parse_and_insert_data(decks):


    for deck in decks:
        deck_id = deck['id']
        author_uid = deck['account_uid']
        author_nickname = deck['nickname']
        deck_title = deck['title']
        creation_time = deck['created_at']

        role_cards = deck['role_cards']
        role_card_CODEs = ''
        role_card_NAMEs = ''
        for role_card in role_cards:
            role_card_CODEs += str(role_card['basic']['item_id']) + ', '
            role_card_NAMEs += str(role_card['basic']['name']) + ', '
        role_card_NAMEs = role_card_NAMEs[:-2]
        role_card_CODEs = role_card_CODEs[:-2]

        action_cards = deck['action_cards']
        action_card_CODEs = ''
        action_card_NAMEs = ''
        for action_card in action_cards:
            action_card_CODEs += str(action_card['basic']['item_id']) + ', '
        action_card_CODEs = action_card_CODEs[:-2]

        description = deck['desc']
        deck_code = deck['card_code']

        # print(deck_code)

        cursor.execute("""INSERT INTO main.hoyolab_decks_eng 
        (author_nickname, role_card_names, deck_code, title, author_uid, description, 
        action_card_codes, role_card_codes, deck_id, next_page_token, creation_time) VALUES 
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                       (author_nickname, role_card_NAMEs, deck_code, deck_title, author_uid, description,
                        action_card_CODEs, role_card_CODEs, deck_id, next_page_token, creation_time))

        sqlite_connection.commit()


decks_counter = 0
sql_counter = 0
next_page_token = ''
label_id = 1
lang = ['en-us', 'zh-cn']
order_by = ['O_LATEST', 'O_HOT']

while label_id != 100:

    payload = '{"order":"'+order_by[0]+'", "next_page_token":"'+next_page_token+'"}'

    if next_page_token != '$##$':
        label_id += 1
    payload = '{"label_id":'+str(label_id)+', "order":"'+order_by[0]+'", "next_page_token":"'+next_page_token+'"}'

    r = requests.post('https://sg-public-api.hoyolab.com/event/cardsquare/index?lang='+lang[0], data=payload).json()

    next_page_token = str(r['data']['next_page_token'])
    # print(next_page_token)
    decks = r['data']['list']

    OK_code = r['message']

    parse_and_insert_data(decks)
    decks_counter += 20
    sql_counter += 20


    print(decks_counter)


print('Итог: '+str(decks_counter)+' дек добавлено')

cursor.close()
