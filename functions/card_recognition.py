import os
import sqlite3

import numpy as np
import cv2


# for image in os.listdir('./img/assets/decks_img/'):
def recognize_deck_img(image_path):

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

    resize_ratio = 0.7
    img = cv2.resize(cv2.imread(f'./img/assets/decks_img/{image_path}', 0), (0, 0), fx=resize_ratio, fy=resize_ratio)
    # img = cv2.imread(f'./img/assets/decks_img/{image}', 0)
    img_copy = img.copy()

    height, width = img.shape[:2]
    # print(height, width)

    crop_top = int(height * 0.103125)
    crop_bottom = int(height * -0.7375)
    crop_left = int(width * 0.284501062)
    crop_right = int(width * -0.308917197)

    img2 = img_copy[crop_top:crop_bottom, crop_left:crop_right]    # обрезать [верх:-низ, слева:-справа
    # img2 = img_copy[132:-947, 268:-291]    # обрезать [верх:-низ, слева:-справа
    for role_card in role_cards:
        card_code = role_card[0]
        card_name = role_card[1]

        # template = cv2.imread(f'./img/assets/templates/role/{card_code}.png', 0)
        template = cv2.resize(cv2.imread(f'./img/assets/templates/role/{card_code}.png', 0), (0, 0), fx=resize_ratio, fy=resize_ratio)
        # template = cv2.imread(f'./img/assets/templates/action/{card_code}.png', 0)

        h, w = template.shape

        method = cv2.TM_CCOEFF_NORMED

        result = cv2.matchTemplate(img2, template, method)
        yloc, xloc = np.where(result >= .85)

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

                for arr in match_percent_arr:
                    if arr[0] == [x, y, w, h]:
                        match_percent = arr[1]

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
                    cv2.putText(img, card_name, (x, y + int(10 * resize_ratio)), cv2.FONT_HERSHEY_COMPLEX, 0.3 * resize_ratio, (255, 255, 255), 1)

                match_percent = str(match_percent) + '%'
                cv2.putText(img, match_percent, (x, y + step + int(10 * resize_ratio)), cv2.FONT_HERSHEY_COMPLEX, 0.3 * resize_ratio, (255, 255, 255), 1)

                role_card_codes.append(card_code)

        # print(f"LEN_ROLE: {len(role_card_codes)}")
        if len(role_card_codes) >= 3:
            # print('---BREAK ROLE')
            break

    crop_top = int(height * 0.3125)
    crop_bottom = int(height * -0.1390625)
    crop_left = int(width * 0.201698514)
    crop_right = int(width * -0.228237792)

    img2 = img_copy[crop_top:crop_bottom, crop_left:crop_right]
    # img2 = img_copy[400:-178, 190:-215]  # 1280 942, обрезать [верх:-низ, слева:-справа]
    for action_card in action_cards:
        card_code = action_card[0]
        card_name = action_card[1]

        # template = cv2.imread(f'./img/assets/templates/role/{card_code}.png', 0)
        template = cv2.resize(cv2.imread(f'./img/assets/templates/action/{card_code}.png', 0), (0, 0), fx=resize_ratio, fy=resize_ratio)
        # template = cv2.imread(f'./img/assets/templates/action/{card_code}.png', 0)

        h, w = template.shape

        method = cv2.TM_CCOEFF_NORMED

        result = cv2.matchTemplate(img2, template, method)
        yloc, xloc = np.where(result >= .815)

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
                        cv2.putText(img, card_name_part, (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.3, (255, 255, 255), 1)
                else:
                    cv2.putText(img, card_name, (x, y + int(10 * resize_ratio)), cv2.FONT_HERSHEY_COMPLEX, 0.3 * resize_ratio, (255, 255, 255), 1)

                match_percent = str(match_percent) + '%'
                cv2.putText(img, match_percent, (x, y + step + int(10 * resize_ratio)), cv2.FONT_HERSHEY_COMPLEX, 0.3 * resize_ratio, (255, 255, 255), 1)

                action_card_codes.append(card_code)
                if len(action_card_codes) >= 30:
                    # print('----BREAK ACTION')
                    break

        # print(f"LEN_ACTION: {len(action_card_codes)}")
        if len(action_card_codes) >= 30:
            # print('----BREAK ACTION')
            break


    # break

    cv2.imwrite(f'./img/assets/result/{image_path}', img)

    # img_str = cv2.imencard_code('.jpg', img)[1].tostring()

    return f'./img/assets/result/{image_path}', role_card_codes, action_card_codes
    # card_counter += 1

    # cv2.imshow(f"///", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # break




    # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
    #     location = min_loc
    # else:
    #     location = max_loc
    #
    # bottom_right = (location[0] + w, location[1] + h)
    # cv2.rectangle(img2, location, bottom_right, 255, 5)
    # cv2.imshow(f"{max_val}//{min_val}", img2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()







# import cv2
# import os
#
#
# def find_features(img1):
#     correct_matches_dct = {}
#     directory = './img/role_cards_low/'
#     for image in os.listdir(directory):
#         img2 = cv2.imread(directory+image, 0)
#         orb = cv2.ORB_create()
#         kp1, des1 = orb.detectAndCompute(img1, None)
#         kp2, des2 = orb.detectAndCompute(img2, None)
#         bf = cv2.BFMatcher()
#         matches = bf.knnMatch(des1, des2, k=2)
#         correct_matches = []
#         for m, n in matches:
#             if m.distance < 0.75*n.distance:
#                 correct_matches.append([m])
#                 correct_matches_dct[image.split('.')[0]] = len(correct_matches)
#     correct_matches_dct = dict(sorted(correct_matches_dct.items(),
#                                key=lambda item: item[1], reverse=True))
#     return list(correct_matches_dct.keys())[0]
#
#
# def find_contours_of_cards(image):
#     blurred = cv2.GaussianBlur(image, (3, 3), 0)
#     T, thresh_img = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)
#     cv2.imshow('Изображение', thresh_img)
#     cv2.waitKey(0)
#     (cnts, _) = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     return cnts
#
#
# def find_coordinates_of_cards(cnts, image):
#     cards_coordinates = {}
#     for i in range(0, len(cnts)):
#         x, y, w, h = cv2.boundingRect(cnts[i])
#         if w > 20 and h > 30:
#             img_crop = image[y - 15:y + h + 15, x - 15:x + w + 15]
#             cards_name = find_features(img_crop)
#             cards_coordinates[cards_name] = (x - 15, y - 15, x + w + 15, y + h + 15)
#     return cards_coordinates
#
#
# def draw_rectangle_aroud_cards(cards_coordinates, image):
#     for key, value in cards_coordinates.items():
#         rec = cv2.rectangle(image, (value[0], value[1]), (value[2], value[3]), (255, 255, 0), 2)
#         cv2.putText(rec, key, (value[0], value[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 1)
#     cv2.imshow('Image', image)
#     cv2.waitKey(0)
#
#
# if __name__ == '__main__':
#     main_image = cv2.imread('./img/deck.jpeg')
#     gray_main_image = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
#     contours = find_contours_of_cards(gray_main_image)
#     cards_location = find_coordinates_of_cards(contours, gray_main_image)
#     print(cards_location)
#     # draw_rectangle_aroud_cards(cards_location, main_image)
