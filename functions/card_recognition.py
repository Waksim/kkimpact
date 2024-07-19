import os
import sqlite3

import numpy as np
import cv2


# for image in os.listdir('./img/assets/decks_img/'):
def recognize_deck_img(image_path, match_rate_role=0, match_rate=0):

    role_card_codes = []
    action_card_codes = []

    card_counter = 0
    sqlite_connection = sqlite3.connect('./tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()

    cursor.execute(f"SELECT code, card_name_ru FROM main.role_cards")
    role_cards = cursor.fetchall()
    cursor.execute(f"SELECT code, card_name_ru FROM main.action_cards")
    action_cards = cursor.fetchall()
    # print(f"Изображение №{image}")

    img = cv2.imread(f'./img/assets/decks_img/{image_path}', 0)
    # img = cv2.imread(f'./img/assets/decks_img/{image}', 0)

    # cv2.imshow('image', img2)
    # cv2.waitKey(0)

    height, width = img.shape[:2]
    print(height, width)
    the_standard = 0

    if 1274 <= int(height) <= 1286 and 934 <= int(width) <= 950:
        resize_ratio_height = 896/height
        resize_ratio_width = 659/width
        resize_ratio = round((resize_ratio_height + resize_ratio_width) / 2, 1)
        the_standard = 1
        print(resize_ratio)
        print('Эталон')

    elif 896 <= int(height) < 1274 and 659 <= int(width) < 934:
        resize_ratio_height = 896 / height
        resize_ratio_width = 659 / width
        resize_ratio = round((resize_ratio_height + resize_ratio_width) / 2, 1)
        print(resize_ratio)
        print('Мелкая шелупонь')
    elif match_rate != 0:
        resize_ratio = 400 / height
        print(resize_ratio)
        print('Фановый режим')
    else:
        resize_ratio_height = 896 / height
        resize_ratio_width = 659 / width
        resize_ratio = round((resize_ratio_height + resize_ratio_width) / 2, 1)
        print(resize_ratio)
        print('Нечисть безразмерная')
        return [0, 0, 0]

    img = cv2.resize(img, (0, 0), fx=resize_ratio, fy=resize_ratio)
    img_copy = img.copy()

    height, width = img.shape[:2]
    print(height, width)

    if the_standard and match_rate == 0:

        crop_top = int(132 * resize_ratio)
        # print('crop_top - ',crop_top)
        crop_bottom = int(-947 * resize_ratio)
        # print('crop_bottom - ',crop_bottom)
        crop_left = int(268 * resize_ratio)
        # print('crop_left - ',crop_left)
        crop_right = int(-291 * resize_ratio)
        # print('crop_right - ',crop_right)

        img2 = img_copy[crop_top:crop_bottom, crop_left:crop_right]    # обрезать [верх:-низ, слева:-справа

    else:
        img2 = img_copy

    # cv2.imshow('image', img2)
    # cv2.waitKey(0)

    # img2 = img_copy[132:-947, 268:-291]    # обрезать [верх:-низ, слева:-справа
    for role_card in role_cards:
        card_code = role_card[0]
        card_name = role_card[1]

        # template = cv2.imread(f'./img/assets/templates/role/{card_code}.png', 0)
        template = cv2.imread(f'./img/assets/templates/role/{card_code}.png', 0)
        # template = cv2.resize(cv2.imread(f'./img/assets/templates/role/{card_code}.png', 0), (0, 0), fx=resize_ratio, fy=resize_ratio)
        # template = cv2.imread(f'./img/assets/templates/action/{card_code}.png', 0)

        h, w = template.shape

        method = cv2.TM_CCOEFF_NORMED

        result = cv2.matchTemplate(img2, template, method)
        if match_rate == 0:
            yloc, xloc = np.where(result >= .85)
        else:
            yloc, xloc = np.where(result >= match_rate_role/100)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        match_percent = str(int(float("%.2f" % round(max_val, 2)) * 100))

        rectangles = []
        match_percent_arr = []
        for (x, y) in zip(xloc, yloc):
            rectangles.append([int(x), int(y), int(w), int(h)])
            rectangles.append([int(x), int(y), int(w), int(h)])
            match_percent_arr.append([[int(x), int(y), int(w), int(h)], match_percent])

        rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

        if len(rectangles) > 0:
            # print(f"{card_code} -- {card_name} -- {len(rectangles)}")
            # [132: -947, 268: -291]
            for (x, y, w, h) in rectangles:

                if card_code in role_card_codes:
                    continue

                for arr in match_percent_arr:
                    if arr[0] == [x, y, w, h]:
                        match_percent = arr[1]
                # if stan
                x += int(268 * resize_ratio)
                y += int(132 * resize_ratio)
                step = int(15 * resize_ratio)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)

                x += int(10 * resize_ratio)
                y += int(30 * resize_ratio)
                if len(card_name) > 9:
                    y -= step

                    card_name_splited = card_name.split()
                    if len(card_name.split()) == 1:
                        if len(card_name.split('-')) > 1:
                            card_name_splited = card_name.split('-')

                    for card_name_part in card_name_splited:
                        y = y + step
                        cv2.putText(img, card_name_part, (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.3 * resize_ratio, (255, 255, 255), 1)
                else:
                    cv2.putText(img, card_name, (x - int(8 * resize_ratio), y + int(10 * resize_ratio)), cv2.FONT_HERSHEY_COMPLEX, 0.5 * resize_ratio, (255, 255, 255), 1)

                match_percent = str(match_percent) + '%'
                cv2.putText(img, match_percent, (x, y + step + int(20 * resize_ratio)), cv2.FONT_HERSHEY_COMPLEX, 0.7 * resize_ratio, (255, 255, 255), 1)

                role_card_codes.append(card_code)

        # print(f"LEN_ROLE: {len(role_card_codes)}")
        if len(role_card_codes) >= 3:
            # print('---BREAK ROLE')
            break

    if the_standard and match_rate == 0:
        crop_top = int(400 * resize_ratio)
        crop_bottom = int(-178 * resize_ratio)
        crop_left = int(190 * resize_ratio)
        crop_right = int(-215 * resize_ratio)

        img2 = img_copy[crop_top:crop_bottom, crop_left:crop_right]

    else:
        img2 = img_copy

    # img2 = img_copy[400:-178, 190:-215]  # 1280 942, обрезать [верх:-низ, слева:-справа]
    for action_card in action_cards:
        card_code = action_card[0]
        card_name = action_card[1]

        # template = cv2.imread(f'./img/assets/templates/role/{card_code}.png', 0)
        # template = cv2.imread(f'./img/assets/templates/action/{card_code}.png', 0)
        template = cv2.resize(cv2.imread(f'./img/assets/templates/action/{card_code}.png', 0), (0, 0), fx=resize_ratio, fy=resize_ratio)
        # template = cv2.imread(f'./img/assets/templates/action/{card_code}.png', 0)

        h, w = template.shape

        method = cv2.TM_CCOEFF_NORMED

        result = cv2.matchTemplate(img2, template, method)
        if match_rate == 0:
            yloc, xloc = np.where(result >= .815)
        else:
            yloc, xloc = np.where(result >= match_rate/100)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        match_percent = str(int(float("%.2f" % round(max_val, 2)) * 100))

        rectangles = []
        match_percent_arr = []
        for (x, y) in zip(xloc, yloc):
            rectangles.append([int(x), int(y), int(w), int(h)])
            rectangles.append([int(x), int(y), int(w), int(h)])
            match_percent_arr.append([[int(x), int(y), int(w), int(h)], match_percent])

        rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

        if len(rectangles) > 0:
            # print(f"{card_code} -- {card_name} -- {len(rectangles)}")
            for (x, y, w, h) in rectangles:

                if action_card_codes.count(card_code) >= 2:
                    print('Continue')
                    continue

                for arr in match_percent_arr:
                    if arr[0] == [x, y, w, h]:
                        match_percent = arr[1]

                x += int(190 * resize_ratio)
                y += int(400 * resize_ratio)
                step = int(15 * resize_ratio)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)

                if len(card_name) > 9:
                    y += int(10 * resize_ratio)
                    y -= step

                    card_name_splited = card_name.split()
                    if len(card_name.split()) == 1:
                        if len(card_name.split('-')) > 1:
                            card_name_splited = card_name.split('-')

                    for card_name_part in card_name_splited:
                        y = y + step
                        cv2.putText(img, card_name_part, (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.3 * resize_ratio, (255, 255, 255), 1)
                else:
                    cv2.putText(img, card_name, (x, y + int(10 * resize_ratio)), cv2.FONT_HERSHEY_COMPLEX, 0.3 * resize_ratio, (255, 255, 255), 1)

                match_percent = str(match_percent) + '%'
                cv2.putText(img, match_percent, (x + int(5 * resize_ratio), y + step + int(15 * resize_ratio)), cv2.FONT_HERSHEY_COMPLEX, 0.5 * resize_ratio, (255, 255, 255), 1)

                action_card_codes.append(card_code)
                if len(action_card_codes) >= 30:
                    # print('----BREAK ACTION')
                    break

        # print(f"LEN_ACTION: {len(action_card_codes)}")
        if len(action_card_codes) >= 30:
            # print('----BREAK ACTION')
            break


    # break

    result_img_path = f'./img/assets/result/{image_path}'

    cv2.imwrite(result_img_path, img)

    return result_img_path, role_card_codes, action_card_codes

