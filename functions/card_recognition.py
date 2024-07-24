import os
import random
import sqlite3

import numpy as np
import cv2


# for image in os.listdir('./img/assets/decks_img/'):
from functions.find_resonance import find_resonance


def cords_in_arr(original_cords, cords_arr):
    x, y, w, h = original_cords

    if [x, y, w, h] in cords_arr:
        return 1

    for i in range(1, 10):

        if [x + i, y, w, h] in cords_arr:
            return 1
        if [x, y + i, w, h] in cords_arr:
            return 1
        if [x + i, y + i, w, h] in cords_arr:
            return 1
        if [x - i, y, w, h] in cords_arr:
            return 1
        if [x - i, y - i, w, h] in cords_arr:
            return 1
        if [x, y - i, w, h] in cords_arr:
            return 1

    return 0


# code, card_name_ru, link_with_char, doublecated, resonance
def delete_from_arr(action_cards, role_card_codes):
    new_list = []

    resonances = find_resonance(role_cards=role_card_codes)

    for action_card in action_cards:

        resonance = action_card[4].lower()
        link_with_char = action_card[2]

        if resonance == '0' or resonance in resonances:
            if link_with_char == 0 or link_with_char in role_card_codes:
                new_list.append(action_card)
                # print(f"{resonances} --- {resonance}")
                # print('OK')

    return new_list


def sort_role_cards(temp_role_card_codes):
    action_card_codes = []

    temp_role_card_codes.sort(key=lambda card: (card[1]))

    for card_info in temp_role_card_codes:
        card_code = card_info[0]
        action_card_codes.append(card_code)

    return action_card_codes


def recognize_deck_img(image_path, match_rate_role=0, match_rate=0, heal_mode=0):

    temp_role_card_codes = []
    role_card_codes = []
    action_card_codes = []

    cords_arr = []

    card_counter = 0
    sqlite_connection = sqlite3.connect('./tcgCodes.sqlite')
    cursor = sqlite_connection.cursor()

    cursor.execute(f"SELECT code, card_name_ru FROM main.role_cards")
    role_cards = cursor.fetchall()
    cursor.execute(f"SELECT code, card_name_ru, link_with_char, doublecated, resonance, weights_hoyolab, weights_kkimpact "
                   f"FROM main.cv_weights")
    action_cards = cursor.fetchall()

    if heal_mode == 1:
        action_cards.reverse()
    if heal_mode == 2:
        random.shuffle(action_cards)

    # print(f"Изображение №{image}")

    img = cv2.imread(f'./img/assets/decks_img/{image_path}', 0)
    # img = cv2.imread(f'./img/assets/decks_img/{image}', 0)
    # print(f'./img/assets/decks_img/{image_path}')

    # cv2.imshow('image', img)
    # cv2.waitKey(0)

    height, width = img.shape[:2]
    print(height, width)
    the_standard = 0

    if 1427 <= int(height) <= 1433 and 799 <= int(width) <= 803:
        # resize_ratio_height = 896/height
        # resize_ratio_width = 659/width
        # resize_ratio = round((resize_ratio_height + resize_ratio_width) / 2, 1)
        resize_ratio = 0.5
        # resize_ratio = 1
        the_standard = 'kkimpact'
        # print('KKIMPACT')

    # elif 1274 <= int(height) <= 1286 and 934 <= int(width) <= 950:
    #     # resize_ratio_height = 896/height
    #     # resize_ratio_width = 659/width
    #     # resize_ratio = round((resize_ratio_height + resize_ratio_width) / 2, 1)
    #     resize_ratio = 0.7
    #     # resize_ratio = 1
    #     the_standard = 'hoyolab'
    #     # print(resize_ratio)
    #     print('Эталон')

    else:
        # 1280 717 0.56015625
        # 1280 942 0.7359375
        # 1091 688 0.6306141154903758
        ratio = width / height
        print(ratio)

        if 0.7 <= ratio <= 0.75:
            the_standard = 'hoyolab'
            print('hoyolab')
            resize_ratio_height = 896 / height
            resize_ratio_width = 659 / width
            resize_ratio = round((resize_ratio_height + resize_ratio_width) / 2, 1)
            print(resize_ratio)
            # resize_ratio = resize_ratio_height
        if 0.5 < ratio < 0.6:
            the_standard = 'kkimpact'
            print('kkimpact')
            resize_ratio_height = 715 / height
            # resize_ratio_width = 400 / width
            # resize_ratio = round((resize_ratio_height + resize_ratio_width) / 2, 1)
            resize_ratio = resize_ratio_height
            # resize_ratio = 0.5
            print(resize_ratio)
        if 0.6 < ratio < 0.65:
            the_standard = 'hoyolab_cropped'
            print('hoyolab_cropped')
            resize_ratio_height = 1004 / height
            resize_ratio = resize_ratio_height
            print(resize_ratio)

    img = cv2.resize(img, (0, 0), fx=resize_ratio, fy=resize_ratio)
    img_copy = img.copy()

    if the_standard == 'kkimpact':
        resize_ratio = 0.55859375
    if the_standard == 'hoyolab':
        resize_ratio = 0.7
    if the_standard == 'hoyolab_cropped':
        resize_ratio = 0.9202566452795601

    height, width = img.shape[:2]
    print(height, width)

    # 50, -1095, 140, -140
    # 40, -980, 120, -120
    # 55, -825, 138, -160
    if the_standard == 'kkimpact' and match_rate == 0:

        crop_top = int(40 * resize_ratio)
        # print('crop_top - ',crop_top)
        # crop_bottom = int(-1095 * resize_ratio)
        crop_bottom = int(-980 * resize_ratio)
        # print('crop_bottom - ',crop_bottom)
        crop_left = int(120 * resize_ratio)
        # print('crop_left - ',crop_left)
        crop_right = int(-120 * resize_ratio)
        # print('crop_right - ',crop_right)

        img2 = img_copy[crop_top:crop_bottom, crop_left:crop_right]  # обрезать [верх:-низ, слева:-справа

    elif the_standard == 'hoyolab' and match_rate == 0:

        crop_top = int(132 * resize_ratio)
        # print('crop_top - ',crop_top)
        crop_bottom = int(-947 * resize_ratio)
        # print('crop_bottom - ',crop_bottom)
        crop_left = int(268 * resize_ratio)
        # print('crop_left - ',crop_left)
        crop_right = int(-291 * resize_ratio)
        # print('crop_right - ',crop_right)

        img2 = img_copy[crop_top:crop_bottom, crop_left:crop_right]    # обрезать [верх:-низ, слева:-справа

    elif the_standard == 'hoyolab_cropped' and match_rate == 0:

        crop_top = int(55 * resize_ratio)
        # print('crop_top - ',crop_top)
        crop_bottom = int(-825 * resize_ratio)
        # print('crop_bottom - ',crop_bottom)
        crop_left = int(138 * resize_ratio)
        # print('crop_left - ',crop_left)
        crop_right = int(-160 * resize_ratio)
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
        # template = cv2.imread(f'./img/assets/templates/role/{card_code}.png', 0)

        if the_standard == 'hoyolab' or the_standard == 'hoyolab_cropped':
            template = cv2.resize(cv2.imread(f'./img/assets/templates/role/{card_code}.png', 0), (0, 0), fx=resize_ratio, fy=resize_ratio)

        if the_standard == 'kkimpact':
            template = cv2.resize(cv2.imread(f'./img/assets/templates/kkimpact_roles/{card_code}.png', 0), (0, 0), fx=resize_ratio, fy=resize_ratio)

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

            for (x, y, w, h) in rectangles:

                if card_code in role_card_codes:
                    continue

                if the_standard == 'hoyolab' or the_standard == 'hoyolab_cropped':
                    modifier = 1
                if the_standard == 'kkimpact':
                    modifier = 2

                default_x = x

                for arr in match_percent_arr:
                    if arr[0] == [x, y, w, h]:
                        match_percent = arr[1]

                # 132, -947, 268, -291
                if the_standard == 'hoyolab':
                    x += int(268 * resize_ratio)
                    y += int(132 * resize_ratio)
                # 55, -825, 138, -160
                if the_standard == 'hoyolab_cropped':
                    x += int(138 * resize_ratio)
                    y += int(55 * resize_ratio)
                # 40, -980, 120, -120
                if the_standard == 'kkimpact':
                    x += int(120 * resize_ratio)
                    y += int(40 * resize_ratio)

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
                        y = y + step * modifier
                        cv2.putText(img, card_name_part, (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5 * resize_ratio * modifier, (255, 255, 255), 1)
                else:
                    cv2.putText(img, card_name, (x - int(8 * resize_ratio), y + int(10 * resize_ratio * modifier)), cv2.FONT_HERSHEY_COMPLEX, 0.5 * resize_ratio * modifier, (255, 255, 255), 1)

                match_percent = str(match_percent) + '%'
                cv2.putText(img, match_percent, (x, y + step + int(20 * resize_ratio * modifier)), cv2.FONT_HERSHEY_COMPLEX, 0.7 * resize_ratio * modifier, (255, 255, 255), 1)

                temp_role_card_codes.append([card_code, default_x])

        # print(f"LEN_ROLE: {len(role_card_codes)}")
        if len(temp_role_card_codes) >= 3:
            # print('---BREAK ROLE')
            break

    role_card_codes = sort_role_cards(temp_role_card_codes)

    result_img_path = f'./img/assets/result/testt.jpeg'

    cv2.imwrite(result_img_path, img)
    # ARENA
    # 170, -960, 450, -210
    if len(role_card_codes) == 0:
        if the_standard == 'hoyolab':
            the_standard = 'hoyolab_arena'
            crop_top = int(170 * resize_ratio)
            # print('crop_top - ', crop_top)
            crop_bottom = int(-960 * resize_ratio)
            # print('crop_bottom - ',crop_bottom)
            crop_left = int(450 * resize_ratio)
            # print('crop_left - ',crop_left)
            crop_right = int(-210 * resize_ratio)
            # print('crop_right - ',crop_right)

            img2 = img_copy[crop_top:crop_bottom, crop_left:crop_right]  # обрезать [верх:-низ, слева:-справа
        # 90, -785, 305, -75
        elif the_standard == 'hoyolab_cropped':
            # crop_top = int(90)
            crop_top = int(90 * resize_ratio)
            # print('crop_top - ', crop_top)
            # crop_bottom = int(-785)
            crop_bottom = int(-785 * resize_ratio)
            # print('crop_bottom - ',crop_bottom)
            # crop_left = int(305)
            crop_left = int(305 * resize_ratio)
            # print('crop_left - ',crop_left)
            # crop_right = int(-75)
            crop_right = int(-75 * resize_ratio)
            # print('crop_right - ',crop_right)
            img2 = img_copy[crop_top:crop_bottom, crop_left:crop_right]
        else:
            img2 = img_copy

        # cv2.imshow('image', img2)
        # cv2.waitKey(0)

        for role_card in role_cards:
            card_code = role_card[0]
            card_name = role_card[1]

            # template = cv2.imread(f'./img/assets/templates/role/{card_code}.png', 0)
            # template = cv2.imread(f'./img/assets/templates/role/{card_code}.png', 0)

            if the_standard == 'hoyolab_arena' or the_standard == 'hoyolab_cropped':
                template = cv2.resize(cv2.imread(f'./img/assets/templates/roles_arena/{card_code}.png', 0), (0, 0),
                                      fx=resize_ratio, fy=resize_ratio)

            # template = cv2.imread(f'./img/assets/templates/action/{card_code}.png', 0)

            h, w = template.shape

            method = cv2.TM_CCOEFF_NORMED

            result = cv2.matchTemplate(img2, template, method)

            if the_standard == 'hoyolab_arena':
                yloc, xloc = np.where(result >= .85)
            if the_standard == 'hoyolab_cropped':
                yloc, xloc = np.where(result >= .83)

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
                # 50, -1095, 140, -140
                # 40, -980, 120, -120

                for (x, y, w, h) in rectangles:

                    if card_code in role_card_codes:
                        continue

                    if the_standard == 'hoyolab_arena':
                        modifier = 1
                    if the_standard == 'hoyolab_cropped':
                        modifier = 1

                    default_x = x

                    for arr in match_percent_arr:
                        if arr[0] == [x, y, w, h]:
                            match_percent = arr[1]

                    # 170, -960, 450, -210
                    if the_standard == 'hoyolab_arena':
                        x += int(450 * resize_ratio)
                        y += int(170 * resize_ratio)
                    # 90, -785, 305, -75
                    if the_standard == 'hoyolab_cropped':
                        x += int(305 * resize_ratio)
                        y += int(90 * resize_ratio)

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
                            y = y + step * modifier
                            cv2.putText(img, card_name_part, (x-5, y), cv2.FONT_HERSHEY_COMPLEX,
                                        0.5 * resize_ratio * modifier, (255, 255, 255), 1)
                    else:
                        cv2.putText(img, card_name, (x - int(8 * resize_ratio), y + int(10 * resize_ratio * modifier)),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5 * resize_ratio * modifier, (255, 255, 255), 1)

                    match_percent = str(match_percent) + '%'
                    cv2.putText(img, match_percent, (x, y + step + int(20 * resize_ratio * modifier)),
                                cv2.FONT_HERSHEY_COMPLEX, 0.7 * resize_ratio * modifier, (255, 255, 255), 1)

                    temp_role_card_codes.append([card_code, default_x])

            # print(f"LEN_ROLE: {len(role_card_codes)}")
            if len(temp_role_card_codes) >= 3:
                # print('---BREAK ROLE')
                break

    # print(temp_role_card_codes)
    role_card_codes = sort_role_cards(temp_role_card_codes)
    # print(role_card_codes)

    # 425, -27, 27, -34
    # 380, -27, 25, -30
    if the_standard == 'kkimpact' and match_rate == 0:
        crop_top = int(380 * resize_ratio)
        crop_bottom = int(-27 * resize_ratio)
        crop_left = int(25 * resize_ratio)
        crop_right = int(-30 * resize_ratio)

        img2 = img_copy[crop_top:crop_bottom, crop_left:crop_right]

    elif the_standard == 'hoyolab' or the_standard == 'hoyolab_arena':
        crop_top = int(400 * resize_ratio)
        crop_bottom = int(-178 * resize_ratio)
        crop_left = int(190 * resize_ratio)
        crop_right = int(-215 * resize_ratio)

        img2 = img_copy[crop_top:crop_bottom, crop_left:crop_right]

    # 328, -60, 60, -86
    elif the_standard == 'hoyolab_cropped':
        crop_top = int(328 * resize_ratio)
        crop_bottom = int(-60 * resize_ratio)
        crop_left = int(60 * resize_ratio)
        crop_right = int(-86 * resize_ratio)

        img2 = img_copy[crop_top:crop_bottom, crop_left:crop_right]

    else:
        img2 = img_copy

    # cv2.imshow('image', img2)
    # cv2.waitKey(0)

    action_cards = delete_from_arr(action_cards, role_card_codes)
    # print(role_card_codes)
    # print(action_cards)


    # img2 = img_copy[400:-178, 190:-215]  # 1280 942, обрезать [верх:-низ, слева:-справа]
    for action_card in action_cards:
        card_code = action_card[0]
        card_name = action_card[1]
        if the_standard == 'hoyolab' or the_standard == 'hoyolab_arena' or the_standard == 'hoyolab_cropped':
            card_weight = action_card[5]
        if the_standard == 'kkimpact':
            card_weight = action_card[6]

        # template = cv2.imread(f'./img/assets/templates/role/{card_code}.png', 0)
        # template = cv2.imread(f'./img/assets/templates/action/{card_code}.png', 0)

        if the_standard == 'hoyolab' or the_standard == 'hoyolab_arena' or the_standard == 'hoyolab_cropped':
            template = cv2.resize(cv2.imread(f'./img/assets/templates/action/{card_code}.png', 0), (0, 0), fx=resize_ratio, fy=resize_ratio)

        if the_standard == 'kkimpact':
            template = cv2.resize(cv2.imread(f'./img/assets/templates/kkimpact_actions/{card_code}.png', 0), (0, 0), fx=resize_ratio, fy=resize_ratio)

        # template = cv2.imread(f'./img/assets/templates/action/{card_code}.png', 0)

        h, w = template.shape

        method = cv2.TM_CCOEFF_NORMED

        result = cv2.matchTemplate(img2, template, method)
        if match_rate == 0:
            yloc, xloc = np.where(result >= card_weight/100)
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
            # print(f"{card_code} -- {card_name} -- {len(rectangles)} -- {card_weight}")
            for (x, y, w, h) in rectangles:
                original_cords = [x, y, w, h]
                if cords_in_arr(original_cords, cords_arr):
                    continue

                if action_card_codes.count(card_code) >= 2:
                    # print('Continue')
                    continue

                for arr in match_percent_arr:
                    if arr[0] == [x, y, w, h]:
                        match_percent = arr[1]

                # 425, -27, 27, -34

                if the_standard == 'hoyolab' or the_standard == 'hoyolab_arena' or the_standard == 'hoyolab_cropped':
                    modifier = 1
                if the_standard == 'kkimpact':
                    modifier = 2

                # 400, -178, 190, -215
                if the_standard == 'hoyolab' or the_standard == 'hoyolab_arena':
                    x += int(190 * resize_ratio)
                    y += int(400 * resize_ratio)
                # 328, -60, 60, -86
                if the_standard == 'hoyolab_cropped':
                    x += int(60 * resize_ratio)
                    y += int(328 * resize_ratio)
                # 380, -27, 25, -30
                if the_standard == 'kkimpact':
                    x += int(25 * resize_ratio)
                    y += int(380 * resize_ratio)

                step = int(15 * resize_ratio * modifier)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)

                if len(card_name) > 9:
                    y += int(10 * resize_ratio * modifier)
                    y -= step

                    card_name_splited = card_name.split()
                    if len(card_name.split()) == 1:
                        if len(card_name.split('-')) > 1:
                            card_name_splited = card_name.split('-')

                    for card_name_part in card_name_splited:
                        y = y + step
                        cv2.putText(img, card_name_part, (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.3 * resize_ratio * modifier, (255, 255, 255), 1)
                else:
                    cv2.putText(img, card_name, (x, y + int(10 * resize_ratio * modifier)), cv2.FONT_HERSHEY_COMPLEX, 0.3 * resize_ratio * modifier, (255, 255, 255), 1)

                match_percent = str(match_percent) + '%'
                cv2.putText(img, match_percent, (x + int(5 * resize_ratio * modifier), y + step + int(15 * resize_ratio * modifier)), cv2.FONT_HERSHEY_COMPLEX, 0.5 * resize_ratio * modifier, (255, 255, 255), 1)

                action_card_codes.append(card_code)

                if len(action_card_codes) >= 30:
                    # print('----BREAK ACTION')
                    break

                cords_arr.append(original_cords)


        # print(f"LEN_ACTION: {len(action_card_codes)}")
        if len(action_card_codes) >= 30:
            # print('----BREAK ACTION')
            break


        # if 1:
        # if 0:
        #     if card_code == 311403:
        #
        #         print(f'\n\nКарт найдено: {action_card_codes.count(card_code)}')
        #
        #         break

# белый двурук, белая кисть, каменное копье, небесная сось
    # break

    result_img_path = f'./img/assets/result/{image_path}'

    cv2.imwrite(result_img_path, img)

    return result_img_path, role_card_codes, action_card_codes

