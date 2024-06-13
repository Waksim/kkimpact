import requests

next_page_token = '$##$65adc170e57860d383877481'

payload = '{"order":"O_LATEST", "next_page_token":"'+next_page_token+'"}'
r = requests.post('https://sg-public-api.hoyolab.com/event/cardsquare/index?lang=ru-ru', data=payload).json()

print(r)

