import sqlite3

sqlite_connection = sqlite3.connect('../tcgCodes.sqlite')
cursor = sqlite_connection.cursor()

cursor.execute("SELECT id, code FROM main.role_cards")
r = cursor.fetchall()

print(r)

for card_info in r:
    card_code = card_info[1]
    id_in_table = card_info[0]
    cursor.execute("UPDATE cv_weights SET link_with_char = ? WHERE link_with_char = ?", (card_code, id_in_table))
    sqlite_connection.commit()

    