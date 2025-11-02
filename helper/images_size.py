from PIL import Image
import os

# Define target size
target_size = (1024, 500)  # Android, Google Play Store
target_size = (1290, 2796)  # iPhonoe, Apple App Store
target_size = (32, 32)  # iPhonoe, Apple App Store

# List of uploaded image paths
input_dir = "../../../Pictures/compress"
input_dir = "./store_preview/new"
input_dir = "../../../Pictures/compress"
new_output_dir = "../../../Pictures/compress"
new_output_dir = "./store_preview/ios"
new_output_dir = "../../../Pictures/new"


def run(input_folder, output_folder, target_size):
    os.makedirs(output_folder, exist_ok=True)
    # Resize and save images
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".png"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            with Image.open(input_path) as img:
                resized_img = img.resize(target_size, Image.LANCZOS)
                new_path = filename.replace(".png", "_resized.png")
                resized_img.save(output_path)


if __name__ == "__main__":
    run(input_dir, new_output_dir, target_size)
