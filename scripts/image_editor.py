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

            if crop_size > 0:
                cropped_img = resized_img.crop((crop_size, crop_size, desired_width - crop_size, desired_height - crop_size))
                cropped_img.save(output_path)
            else:
                resized_img.save(output_path)
    print("Готово!")
    print(output_folder)


resize_ratio = 1
# resize_ratio = 0.7

# create_templates_for_recognize(
#     input_folder="../img/action_cards_lowest_border",
#     output_folder="../img/assets/templates/kkimpact_actions",
#     desired_height=int(160 * resize_ratio),
#     crop_size=int(8 * resize_ratio)
# )
# create_templates_for_recognize(
#     input_folder="../img/role_cards_lowest_border",
#     output_folder="../img/assets/templates/roles_arena",
#     desired_height=int(125 * resize_ratio),
#     crop_size=int(8 * resize_ratio)
# )
# create_templates_for_recognize(
#     input_folder="../img/role_cards_lowest_border",
#     output_folder="../img/assets/templates/kkimpact_roles",
#     desired_height=int(230 * resize_ratio),
#     crop_size=int(10 * resize_ratio)
# )
# create_templates_for_recognize(
#     input_folder="../img/role_cards_lowest_border",
#     output_folder="../img/assets/templates/roles_arena",
#     desired_height=int(339 * resize_ratio),
#     crop_size=0
# )