import sqlite3


async def get_card_number_by_sticker(sticker_uid):
    sqlite_connection = sqlite3.connect('../tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()

    cursor.execute(f"SELECT code FROM main.role_cards WHERE sticker_uid = '{sticker_uid}'")
    r = cursor.fetchall()
    if len(r) == 0:
        return 0
    else:
        card_code = r[0][0]
        cursor.close()
        return card_code
