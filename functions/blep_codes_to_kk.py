import sqlite3



def blep_codes_to_kk(blep_role_cards, blep_action_cards):

    sqlite_connection = sqlite3.connect('./tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()
    role_cards = []
    action_cards = []

    for brole in blep_role_cards:
        cursor.execute(f"SELECT code FROM main.role_cards WHERE blep_code = {brole}")
        role_cards.append(cursor.fetchall()[0][0])

    for baction in blep_action_cards:
        cursor.execute(f"SELECT code FROM main.action_cards WHERE blep_code = {baction}")
        action_cards.append(cursor.fetchall()[0][0])

    return [role_cards, action_cards]

