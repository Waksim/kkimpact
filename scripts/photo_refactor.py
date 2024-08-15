from PIL import Image, ImageOps
# import io
# from aiogram.types import BufferedInputFile
# import sqlite3
# import os
#
#
#
# def do_sticker(img_path, img_name):
#     full_path = img_path+img_name
#     img = Image.open(full_path).convert("RGBA")
#
#     # print(os.stat(full_path).st_size)
#
#     # print(img.size)
#     #
#     new_image = ImageOps.pad(img, (512, 512), method=Image.LANCZOS)
#     # print(new_image.size)
#     # new_image.show()
#
#     new_image.save(f'img/role_cards_stickers/{img_name}')
#
# sqlite_connection = sqlite3.connect('tcgCodes.sqlite')
# cursor = sqlite_connection.cursor()
#
# cursor.execute("SELECT code FROM main.role_cards WHERE sticker_uid = 0")
# codes = cursor.fetchall()
#
# print(len(codes))
#
# for code in codes:
#     do_sticker('img/role_cards_border/', f'{code[0]}.png')
#     print(code[1].split(', ')[0])
#
#
# do_sticker(f'img/role_cards_stickers/', '1411.png')