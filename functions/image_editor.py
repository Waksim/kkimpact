

from PIL import Image
import os


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

            cropped_img = resized_img.crop((crop_size, crop_size, desired_width - crop_size, desired_height - crop_size))

            cropped_img.save(output_path)


create_templates_for_recognize(
    input_folder="../img/action_cards",
    output_folder="../img/assets/templates/action",
    desired_height=124,
    crop_size=8
)
create_templates_for_recognize(
    input_folder="../img/role_cards",
    output_folder="../img/assets/templates/role",
    desired_height=186,
    crop_size=10
)