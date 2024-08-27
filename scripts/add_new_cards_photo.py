from PIL import Image, ImageFilter
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
def border_and_size(input_folder, output_folder, border_image_path, new_width):

    # Создание папки для результатов, если она не существует
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.webp'):
            # Открытие изображения и border.png
            image_path = os.path.join(input_folder, filename)
            image = Image.open(image_path)
            border = Image.open(border_image_path)

            # Изменение размера границы до размера исходного изображения
            border_resized = border.resize(image.size, Image.Resampling.LANCZOS)

            # Наложение border.png на изображение
            combined_image = Image.alpha_composite(image.convert('RGBA'), border_resized.convert('RGBA'))

            # Изменение размера итогового изображения
            width, height = combined_image.size

            new_height = int((new_width / width) * height)
            resized_image = combined_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Сохранение результата в папку "res_role"
            output_path = os.path.join(output_folder, f'{os.path.splitext(filename)[0]}.png')
            resized_image.save(output_path, format='PNG')  # Сохраняем как PNG для сохранения альфа-канала


# ROLE карты
border_and_size(
    input_folder='../img/refactor/role',
    output_folder='../img/role_cards_lowest_border',
    border_image_path='../img/border.png',
    new_width=151
)
print('ROLE карты добавлены!')

# ACTION карты
border_and_size(
    input_folder='../img/refactor/action',
    output_folder='../img/action_cards_lowest_border',
    border_image_path='../img/border.png',
    new_width=105
)
print('ACTION карты добавлены!')


# FOR CV

# KK_ROLE карты
create_templates_for_recognize(
    input_folder="../img/role_cards_lowest_border",
    output_folder="../img/assets/templates/kkimpact_roles",
    desired_height=230,
    crop_size=10
)
print('KK_ROLE карты добавлены!')

# KK_ACTION карты
create_templates_for_recognize(
    input_folder="../img/action_cards_lowest_border",
    output_folder="../img/assets/templates/kkimpact_actions",
    desired_height=160,
    crop_size=8
)
print('KK_ACTION карты добавлены!')

# ARENA_ROLE карты
create_templates_for_recognize(
    input_folder="../img/role_cards_lowest_border",
    output_folder="../img/assets/templates/roles_arena",
    desired_height=125,
    crop_size=8
)
print('ARENA_ROLE карты добавлены!')

# BASE_ROLE карты
create_templates_for_recognize(
    input_folder="../img/role_cards_lowest_border",
    output_folder="../img/assets/templates/role",
    desired_height=182,
    crop_size=8
)
print('BASE_ROLE карты добавлены!')

# BASE_ACTION карты
create_templates_for_recognize(
    input_folder="../img/action_cards_lowest_border",
    output_folder="../img/assets/templates/action",
    desired_height=124,
    crop_size=8
)
print('BASE_ACTION карты добавлены!')

print('- END SCRIPT -')
