import requests


def decrypt_code(code):

    payload = '"code": "'+str(code)+'"'.format()
    url = 'https://sg-public-api.hoyolab.com/event/cardsquare/decode_card_code?lang=en-us'
    payload = '{'+payload+'}'
    r = requests.post(url, data=payload).json()

    role_cards_arr = r['data']['role_cards']
    role_cards_ids = []
    action_cards_arr = r['data']['action_cards']
    action_cards_ids = []

    for role_card in role_cards_arr:
        role_cards_ids.append(role_card['basic']['item_id'])

    for action_card in action_cards_arr:
        action_cards_ids.append(action_card['basic']['item_id'])

    return role_cards_ids, action_cards_ids



# print(decrypt_code('AWDQ5hoPAhDw8VkPCiCw8rQPCzBQ9LUPC0Bg9bgPDGAg9sMPDHCA/MsQDqFQC+UQDrAA'))