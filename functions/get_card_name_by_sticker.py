from db.base import KkiDb


async def get_card_number_by_sticker(sticker_uid):
    database = KkiDb()
    r = database.get_role_card_code_by_sticker_uid(sticker_uid)
    if len(r) == 0:
        return 0
    else:
        card_code = r[0][0]
        return card_code
