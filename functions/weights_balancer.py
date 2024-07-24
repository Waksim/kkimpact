import io
import sqlite3
import time

import PIL.Image as Image

from functions.card_recognition import recognize_deck_img
from functions.create_image import create_decks_img

start_time = time.time()

# debug_photo_path, role_card_codes, action_card_codes = recognize_deck_img(r'test2.jpeg')


def cv_weights_heal(test_img_path, heal_mode, reverse_counter):
    debug_photo_path, role_card_codes, action_card_codes = recognize_deck_img(
        image_path=test_img_path,
        heal_mode=heal_mode
    )

    sqlite_connection = sqlite3.connect('./tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()

    cards_with_new_weights = []
    for action_card_code in action_card_codes:
        if action_card_codes.count(action_card_code) == 2 and action_card_code not in cards_with_new_weights:

            cursor.execute("SELECT weights FROM cv_weights WHERE code = ?", (action_card_code,))
            old_weight = cursor.fetchall()[0][0]

            cursor.execute("UPDATE cv_weights SET weights = ? WHERE code = ?",
                           (old_weight+1, action_card_code))
            sqlite_connection.commit()

            cards_with_new_weights.append(action_card_code)
            print(f'{action_card_code} -- {old_weight} --> {old_weight+1}')
    print(f"{len(cards_with_new_weights)} КАРТ ПРОЛЕЧЕНО!")

    if len(cards_with_new_weights) > 0:
        reverse_counter = cv_weights_heal(test_img_path, heal_mode, reverse_counter+1)
    if heal_mode < 2:
        reverse_counter = cv_weights_heal(test_img_path, heal_mode+1, reverse_counter+1)

    return reverse_counter


reverse_counter = 0
for i in range(1, 11):
    test_img_path = f'{i}.jpeg'
    print(test_img_path)
    reverse_counter = cv_weights_heal(test_img_path, 0, 0)

# for test_img_path in ['14.jpeg']:
    debug_photo_path, role_card_codes, action_card_codes = recognize_deck_img(
            image_path=test_img_path
        )
    photo = create_decks_img(role_cards=role_card_codes, action_cards=action_card_codes, path_for_save=f'./img/assets/result/IMG_{test_img_path}')
# print(photo)

# print(len(action_card_codes))

# recognize_deck_img(r'test.jpg')

# debug_photo_path, role_card_codes, action_card_codes = recognize_deck_img(image_name)

print(f'\n\n{reverse_counter} иттераций')
print("--- %s seconds ---" % (round(time.time() - start_time, 2)))