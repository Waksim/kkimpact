from PIL import Image
import os

input_dir = "/Users/mk/PycharmProjects/gitcg-draft/public/assets1/"
output_dir = "/Users/mk/PycharmProjects/gitcg-draft/public/assets/"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for filename in os.listdir(input_dir):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        img = Image.open(os.path.join(input_dir, filename))
        width, height = img.size
        new_size = (int(width * 0.5), int(height * 0.5))
        resized_img = img.resize(new_size)
        resized_img.save(os.path.join(output_dir, filename))

print("All images resized and saved to", output_dir)