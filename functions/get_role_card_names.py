import sqlite3

sqlite_connection = sqlite3.connect('./tcgCodes.sqlite')
cursor = sqlite_connection.cursor()


def get_role_card_names(role_cards, lang):
    role_card_string = ''
    for role_card in role_cards:
        role_card_string += 'code = ' + str(role_card) + ' OR '

    role_card_string = role_card_string[:-4]

    cursor.execute(f"SELECT card_name_{lang} FROM main.role_cards WHERE {role_card_string}")
    r = cursor.fetchall()

    names_line = ''
    for name in r:
        names_line += name[0] + ', '

    return names_line[:-2]



get_role_card_names([1101, 1102, 1103], 'ru')