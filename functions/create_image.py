from PIL import Image, ImageDraw, ImageFont
from functions.find_resonance import find_resonance
from functions.decryption_of_the_code import decrypt_code
import io
from aiogram.types import BufferedInputFile


def create_decks_img(deck_code='', role_cards=[], action_cards=[]):
    if deck_code != '':
        r = decrypt_code(deck_code)
        role_cards = r[0]
        action_cards = r[1]
        resonances = find_resonance(role_cards=role_cards)
    else:
        resonances = find_resonance(role_cards=role_cards)

    im0 = Image.open('../img/background.png').convert("RGBA")

    x = 37
    y = 435
    c = 0

    for action_card in action_cards:
        if c == 6:
            x = 37
            y += 194
            c = 0
        im1 = Image.open(f'img/action_cards_lowest_border/{action_card}.png').convert("RGBA")
        im0.paste(im1, (x, y), im1)

        x += 123
        c += 1
        im1.close()

    x = 150

    for role_card in role_cards:
        im1 = Image.open(f'img/role_cards_lowest_border/{role_card}.png').convert("RGBA")
        # width, height = im1.size
        # print(width, height)
        # im1 = im1.resize((int(151), int(259)), resample=Image.BOX)

        # width, height = im1.size
        # print(width,height)

        im0.paste(im1, (x, 64), im1)

        x += 175
        im1.close()

    res_len = len(resonances)

    if res_len == 0:
        im1 = Image.open(f'../img/resonance/non_res1.png').convert("RGBA")
        im0.paste(im1, (314, 358), im1)
        im1.close()

    x1 = 314
    x2 = 212
    x3 = 112
    y = 358
    for resonance in resonances:
        im1 = Image.open(f'img/resonance/{resonance}.png').convert("RGBA")

        if res_len == 3:
            im0.paste(im1, (x3, y), im1)
            x3 += 202

        if res_len == 1:
            im0.paste(im1, (x1, y), im1)

        if res_len == 2:
            im0.paste(im1, (x2, y), im1)
            x2 += 202

        im1.close()

    im0 = im0.convert("RGB")
    # im0.show()
    temp = io.BytesIO()
    im0.save(temp, 'JPEG')
    # temp.seek(0)

    photo = BufferedInputFile(temp.getvalue(), filename="file.txt")

    im0.close()
    temp.close()

    return photo


def create_draft_tail_img(stage: int, card_code, filename: str, nickname1=0, nickname2=0, resonance1=None, resonance2=None):
    if resonance1 is None:
        resonance1 = ['non_res1']
    if resonance2 is None:
        resonance2 = ['non_res1']
    im2 = Image.open(f'../img/draft_tail/draft_add_card.png').convert("RGBA")
    # stage = 6
    if stage == 99:
        im0 = Image.open(f'../img/draft_tail/background.png').convert("RGBA")
        im0.paste(im2, (344, 142), im2)
    else:
        im0 = Image.open(f'img/draft_tail/temp/{filename}.png').convert("RGBA")
        im1 = Image.open(f'img/avatars_lowest/{card_code}.png').convert("RGBA")
        if stage == 0:
            print('in stage 0')
            im0.paste(im1, (260, 58), im1)
            im0.paste(im2, (675, 142), im2)
            # x = 344, y = 142, different = 85
        if stage == 1:
            # 1 бан II игрока
            im0.paste(im1, (591, 58), im1)
            im0.paste(im2, (674, 328), im2)
        if stage == 2:
            # 1 пик II игрока
            im0.paste(im1, (590, 244), im1)
            im0.paste(im2, (193, 142), im2)
        if stage == 3:
            # 2 бан I игрока
            im0.paste(im1, (108, 58), im1)
            im0.paste(im2, (344, 328), im2)
        if stage == 4:
            # 1 пик I игрока
            im0.paste(im1, (260, 244), im1)
            im0.paste(im2, (826, 142), im2)
        if stage == 5:
            # 2 бан II игрока
            im0.paste(im1, (742, 58), im1)
            im0.paste(im2, (826, 328), im2)
        if stage == 6:
            # 2 пик II игрока
            im0.paste(im1, (742, 243), im1)
            im0.paste(im2, (192, 328), im2)
        if stage == 7:
            # 2 пик I игрока
            im0.paste(im1, (108, 243), im1)
            im0.paste(im2, (41, 328), im2)
        if stage == 8:
            # 3 пик I игрока
            im0.paste(im1, (-43, 243), im1)
            im0.paste(im2, (976, 328), im2)
        if stage == 9:
            # 3 пик II игрока
            im0.paste(im1, (892, 243), im1)

    if nickname1 != 0:
        draw = ImageDraw.Draw(im0)
        font = ImageFont.truetype("gi_font.ttf", 30)
        w1 = draw.textlength(nickname1, font)
        w2 = draw.textlength(nickname2, font)
        draw.text((258 - w1/2, 68), nickname1, (240, 233, 218), font=font)
        draw.text((891 - w2/2, 68), nickname2, (240, 233, 218), font=font)
    if len(resonance1) != 0:
        x = 298
        for res in resonance1:
            im_res = Image.open(f'img/resonance/{res}.png').convert("RGBA")
            im0.paste(im_res, (x, 514), im_res)
            x = x - 197
    if len(resonance2) != 0:
        x = 675
        for res in resonance2:
            im_res = Image.open(f'img/resonance/{res}.png').convert("RGBA")
            im0.paste(im_res, (x, 514), im_res)
            x = x + 193


    im0.save(f"img/draft_tail/temp/{filename}.png")
    im0 = im0.convert("RGB")
    im0.save(f"img/draft_tail/temp/pupsik.jpg")
    # im0.show()
    temp = io.BytesIO()
    im0.save(temp, 'JPEG')
    # temp.seek(0)

    photo = BufferedInputFile(temp.getvalue(), filename="file.txt")
    # photo = temp.getvalue()

    im0.close()
    temp.close()

    return photo


# create_draft_tail_img(0, 1307, 'filename')
# create_draft_tail_img(9, 1101, 'vdfvd', resonance1=['sumeru', 'frost'], resonance2=['pyro', 'monster', 'fatui'])
# create_draft_tail_img(99, None, 'vdfvd', 'MK', 'АришулечкА Сакова')

    #     im1 = Image.open(f'img/resonance/non_res1.png').convert("RGBA")
    #     im0.paste(im1, (314, 358), im1)
    #     im1.close()
    #
    # x1 = 314
    # x2 = 212
    # x3 = 112
    # y = 358
    # for resonance in resonances:
    #     im1 = Image.open(f'img/resonance/{resonance}.png').convert("RGBA")
    #
    #     if res_len == 3:
    #         im0.paste(im1, (x3, y), im1)
    #         x3 += 202
    #
    #     if res_len == 1:
    #         im0.paste(im1, (x1, y), im1)
    #
    #     if res_len == 2:
    #         im0.paste(im1, (x2, y), im1)
    #         x2 += 202
    #
    #     im1.close()
    #
    #
    # im0 = im0.convert("RGB")
    # temp = io.?edInputFile(temp.getvalue(), filename="file.txt")

    # temp.close()

    # return photo


