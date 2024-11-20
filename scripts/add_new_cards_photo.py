from PIL import Image, ImageFilter, ImageDraw
import os


# Обрезание фото и ресайз для CV
def create_templates_for_recognize(input_folder, output_folder, desired_height, crop_size):

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    for filename in os.listdir(input_folder):
        if filename == '.DS_Store':
            continue
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        with Image.open(input_path) as img:
            width, height = img.size
            desired_width = int(desired_height * width / height)
            resized_img = img.resize((desired_width, desired_height))

            if crop_size > 0:
                cropped_img = resized_img.crop((crop_size, crop_size, desired_width - crop_size, desired_height - crop_size))
                cropped_img.save(output_path)
            else:
                resized_img.save(output_path)


# Наложение рамки и изменение размера
def border_and_size(input_folder, output_folder, border_image_path, new_height):

    # Создание папки для результатов, если она не существует
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.webp'):
            # Открытие изображения и border.png
            image_path = os.path.join(input_folder, filename)
            image = Image.open(image_path)
            if border_image_path != 0:
                border = Image.open(border_image_path)

                # Изменение размера границы до размера исходного изображения
                border_resized = border.resize(image.size, Image.Resampling.LANCZOS)

                # Наложение border.png на изображение
                combined_image = Image.alpha_composite(image.convert('RGBA'), border_resized.convert('RGBA'))
            else:
                combined_image = image

            # Изменение размера итогового изображения
            width, height = combined_image.size

            new_width = int(width * (new_height / height))
            resized_image = combined_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Сохранение результата в папку "res_role"
            output_path = os.path.join(output_folder, f'{os.path.splitext(filename)[0]}.png')
            resized_image.save(output_path, format='PNG')  # Сохраняем как PNG для сохранения альфа-канала


def resize_images(input_folder, output_folder, scale):
    """
    Уменьшает изображения в указанной директории на заданный коэффициент и сохраняет их в другой директории.

    :param input_folder: Путь к директории с исходными изображениями.
    :param output_folder: Путь к директории для сохранения уменьшенных изображений.
    :param scale: Коэффициент уменьшения изображений (по умолчанию 0.5).
    """
    # Убедитесь, что директория для сохранения существует
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Проходим по всем файлам в директории с изображениями
    for filename in os.listdir(input_folder):
        # Полный путь к изображению
        input_path = os.path.join(input_folder, filename)

        # Проверяем, что это файл изображения
        if os.path.isfile(input_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')):
            # Открываем изображение
            with Image.open(input_path) as img:
                # Получаем размеры изображения
                width, height = img.size

                # Уменьшаем изображение
                new_size = (int(width * scale), int(height * scale))
                resized_img = img.resize(new_size, Image.LANCZOS)

                # Полный путь для сохранения уменьшенного изображения
                output_path = os.path.join(output_folder, filename)

                # Сохраняем уменьшенное изображение
                resized_img.save(output_path)


def avatars_builder(input_folder, output_folder):
    # Убедимся, что папка для сохранения результатов существует
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('png', 'jpg', 'jpeg', 'webp')):
            input_path = os.path.join(input_folder, filename)

            # Открываем изображение
            img = Image.open(input_path).convert("RGBA")

            # Определяем размеры нового изображения 300x300
            crop_size = 300
            center_crop = (img.width // 2 - crop_size // 2, 0,
                           img.width // 2 + crop_size // 2, crop_size)
            cropped_img = img.crop(center_crop)

            # Увеличиваем размер маски для сглаживания (например, в 4 раза)
            upscale_factor = 4
            upscale_size = (crop_size * upscale_factor, crop_size * upscale_factor)
            high_res_mask = Image.new("L", upscale_size, 0)
            draw = ImageDraw.Draw(high_res_mask)

            # Рисуем круг увеличенного размера
            circle_radius = (129 // 2) * upscale_factor
            circle_center = (upscale_size[0] // 2, upscale_size[1] // 2)
            draw.ellipse([
                (circle_center[0] - circle_radius, circle_center[1] - circle_radius),
                (circle_center[0] + circle_radius, circle_center[1] + circle_radius)
            ], fill=255)

            # Уменьшаем маску до целевого размера 300x300
            mask = high_res_mask.resize((crop_size, crop_size), Image.Resampling.LANCZOS)

            # Применяем сглаженную маску к обрезанному изображению
            result = Image.new("RGBA", (crop_size, crop_size), (0, 0, 0, 0))
            result.paste(cropped_img, (0, 0), mask=mask)

            # Сохраняем результат в формате PNG
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.png")
            result.save(output_path)


# # ROLE карты
# border_and_size(
#     input_folder='../img/refactor/role',
#     output_folder='../img/role_cards_lowest_border',
#     border_image_path='../img/border.png',
#     new_height=258
# )
# print('ROLE карты добавлены!')
#
# # ACTION карты
# border_and_size(
#     input_folder='../img/refactor/action',
#     output_folder='../img/action_cards_lowest_border',
#     border_image_path='../img/border.png',
#     new_height=180
# )
# print('ACTION карты добавлены!')
#
#
# # FOR CV
#
# # KK_ROLE карты
# create_templates_for_recognize(
#     input_folder="../img/role_cards_lowest_border",
#     output_folder="../img/assets/templates/kkimpact_roles",
#     desired_height=230,
#     crop_size=10
# )
# print('KK_ROLE карты добавлены!')
#
# # KK_ACTION карты
# create_templates_for_recognize(
#     input_folder="../img/action_cards_lowest_border",
#     output_folder="../img/assets/templates/kkimpact_actions",
#     desired_height=160,
#     crop_size=8
# )
# print('KK_ACTION карты добавлены!')
#
# # KK_AVATARS карты
# avatars_builder(
#     input_folder="../img/refactor/role",
#     output_folder="../img/avatars_lowest"
# )
# print('KK_AVATARS карты добавлены!')
#
# # ARENA_ROLE карты
# create_templates_for_recognize(
#     input_folder="../img/role_cards_lowest_border",
#     output_folder="../img/assets/templates/roles_arena",
#     desired_height=125,
#     crop_size=8
# )
# print('ARENA_ROLE карты добавлены!')
#
# # BASE_ROLE карты
# create_templates_for_recognize(
#     input_folder="../img/role_cards_lowest_border",
#     output_folder="../img/assets/templates/role",
#     desired_height=182,
#     crop_size=8
# )
# print('BASE_ROLE карты добавлены!')
#
# # BASE_ACTION карты
# create_templates_for_recognize(
#     input_folder="../img/action_cards_lowest_border",
#     output_folder="../img/assets/templates/action",
#     desired_height=124,
#     crop_size=8
# )
# print('BASE_ACTION карты добавлены!')


# BLEP

# # BLEP_BIG карты
# border_and_size(
#     input_folder="../img/refactor/BLEPS",
#     output_folder="../img/refactor/res_BLEPS_big",
#     border_image_path='../img/border.png',
#     new_height=738
# )
# print('BLEP_BIG карты добавлены!')

# # BLEP_RESIZE карты
# resize_images(
#     input_folder="../img/refactor/BLEPS_big_all",
#     output_folder="/Users/mk/PycharmProjects/gitcg-draft/public/assets/",
#     scale=0.45
# )
# print('BLEP_RESIZE карты добавлены!')
#
# print('- END SCRIPT -')
