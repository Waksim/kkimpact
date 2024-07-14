import os
import sqlite3

import numpy as np
import cv2


sqlite_connection = sqlite3.connect('../tcgCodes.sqlite')
cursor = sqlite_connection.cursor()

cursor.execute(f"SELECT code, card_name_ru FROM main.role_cards")
role_cards = cursor.fetchall()
cursor.execute(f"SELECT code, card_name_ru FROM main.action_cards")
action_cards = cursor.fetchall()
card_counter = 0

for image in os.listdir('../img/assets/decks_img/'):
    print(f"Изображение №{image}")

    img = cv2.imread(f'../img/assets/decks_img/{image}', 0)
    img_copy = img.copy()

    img2 = img_copy[132:-947, 268:-291]
    for role_card in role_cards:
        code = role_card[0]
        card_name = role_card[1]

        template = cv2.imread(f'../img/assets/templates/role/{code}.png', 0)
        # template = cv2.imread(f'../img/assets/templates/action/{code}.png', 0)

        h, w = template.shape

        method = cv2.TM_CCOEFF_NORMED

        result = cv2.matchTemplate(img2, template, method)
        yloc, xloc = np.where(result >= .85)

        rectangles = []
        for (x, y) in zip(xloc, yloc):
            rectangles.append([int(x), int(y), int(w), int(h)])
            rectangles.append([int(x), int(y), int(w), int(h)])

        rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

        if len(rectangles) > 0:
            print(f"{code} -- {card_name} -- {len(rectangles)}")
            # [132: -947, 268: -291]
            for (x, y, w, h) in rectangles:
                x += 268
                y += 132
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
                cv2.putText(img, card_name, (x, y + 10), cv2.FONT_HERSHEY_COMPLEX, 0.3, (255, 255, 255), 1)


    img2 = img_copy[400:-178, 190:-215]
    for action_card in action_cards:
        code = action_card[0]
        card_name = action_card[1]

        # template = cv2.imread(f'../img/assets/templates/role/{code}.png', 0)
        template = cv2.imread(f'../img/assets/templates/action/{code}.png', 0)

        h, w = template.shape

        method = cv2.TM_CCOEFF_NORMED

        result = cv2.matchTemplate(img2, template, method)
        yloc, xloc = np.where(result >= .80)

        rectangles = []
        for (x, y) in zip(xloc, yloc):
            rectangles.append([int(x), int(y), int(w), int(h)])
            rectangles.append([int(x), int(y), int(w), int(h)])

        rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

        if len(rectangles) > 0:
            print(f"{code} -- {card_name} -- {len(rectangles)}")

            for (x, y, w, h) in rectangles:
                x += 190
                y += 400
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
                cv2.putText(img, card_name, (x, y+10), cv2.FONT_HERSHEY_COMPLEX, 0.3, (255,255,255), 1)

    # break

    cv2.imwrite(f'../img/assets/result/find_cards{card_counter}.jpg', img)
    card_counter += 1

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
#     directory = '../img/role_cards_low/'
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
#     main_image = cv2.imread('../img/deck.jpeg')
#     gray_main_image = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
#     contours = find_contours_of_cards(gray_main_image)
#     cards_location = find_coordinates_of_cards(contours, gray_main_image)
#     print(cards_location)
#     # draw_rectangle_aroud_cards(cards_location, main_image)
