from db.base import KkiDb


def get_role_card_names(role_cards, lang):
    role_card_string = ''
    for role_card in role_cards:
        role_card_string += 'code = ' + str(role_card) + ' OR '

    role_card_string = role_card_string[:-4]

    database = KkiDb()
    r = database.get_role_card_names(role_card_string, lang)

    names_line = ''
    for name in r:
        names_line += name[0] + ', '

    return names_line[:-2]



get_role_card_names([1101, 1102, 1103], 'ru')