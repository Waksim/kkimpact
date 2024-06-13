import requests
import sqlite3


sqlite_connection = sqlite3.connect('../tcgCodes.sqlite')
cursor = sqlite_connection.cursor()


def translate(to_lang, text):

    IAM_TOKEN = '<TOKEN>'
    folder_id = '<FOLDER_ID>'
    target_language = to_lang
    texts = text

    body = {
        "targetLanguageCode": target_language,
        "texts": texts,
        "folderId": folder_id,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key {0}".format(IAM_TOKEN)
    }

    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                             json=body,
                             headers=headers
                             ).json()



    return response['translations'][0]['text']

def insert_and_translate():
    cursor.execute('SELECT * FROM main.hoyolab_decks_ru')
    rows = cursor.fetchall()
    for row in rows:

        description_tr = translate('uk', row[6])

        cursor.execute("""INSERT INTO main.hoyolab_decks_ua
                (author_nickname, role_card_names, deck_code, title, author_uid, description,
                action_card_codes, role_card_codes, deck_id, next_page_token, creation_time) VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                       (row[1], row[2], row[3], row[4], row[5], description_tr,
                        row[7], row[8], row[9], row[10], row[11]))

        sqlite_connection.commit()


cursor.execute('SELECT * FROM main.hoyolab_decks_ua')
rows = cursor.fetchall()
for row in rows:
    primary_id = row[0]
    role_card_names = row[2]
    role_card_names_tr = translate('uk', role_card_names)
    cursor.execute('''UPDATE hoyolab_decks_ua SET role_card_names = ? WHERE id = ?''', (role_card_names_tr, primary_id))
    sqlite_connection.commit()
    print(primary_id, ' - ', role_card_names_tr)
cursor.close()
