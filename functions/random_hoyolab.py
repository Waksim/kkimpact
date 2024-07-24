import requests
import json
import sqlite3
import re
import random


def get_random_code_from_hoyolab(table_lang):

    sqlite_connection = sqlite3.connect('./tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()

    cursor.execute(f'SELECT * FROM {table_lang} ORDER BY RANDOM() LIMIT 1;')
    deck_row = cursor.fetchall()[0]

    role_cards_codes = deck_row[8].split(", ")
    action_cards_codes = deck_row[7].split(", ")

    author_nickname = deck_row[1]
    role_card_names = deck_row[2]
    deck_code = deck_row[3]
    deck_title = deck_row[4]
    author_uid = deck_row[5]
    description = deck_row[6]
    creation_time = deck_row[11]

    author_uid_len_1 = int(author_uid[0])

    if author_uid_len_1 == 0:
        server = 'miHoYo'
    if 1 <= author_uid_len_1 <= 5:
        server = 'CN'
    if author_uid_len_1 == 6:
        server = 'A'
    if author_uid_len_1 == 7:
        server = 'EU'
    if author_uid_len_1 == 8:
        server = 'ASIA'
    if author_uid_len_1 == 9:
        server = 'TW'

    cursor.close()

    return [author_nickname, role_card_names, deck_code, deck_title, author_uid, description, creation_time, server,
            role_cards_codes, action_cards_codes]


# get_random_code_from_hoyolab(table_lang='hoyolab_decks_ru')
