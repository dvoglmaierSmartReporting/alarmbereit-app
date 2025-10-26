from PIL import Image, ImageOps
import os

# Define input and output directories
input_dir = "./app/assets/tools"
input_dir = "/Users/dominikvoglmaier/Pictures/compress"
input_dir = "../app/assets/todo"
new_output_dir = "../app/assets/new"
max_size_kb = 100

os.makedirs(new_output_dir, exist_ok=True)


# Function to convert and compress images (PNG → JPG, JPG → JPG) under max_size_kb
def compress_image(input_path, output_path, max_size_kb):
    quality = 85  # start with high quality
    while quality > 10:
        with Image.open(input_path) as img:
            # Correct orientation using EXIF data if present
            img = ImageOps.exif_transpose(img)
            img = img.convert("RGB")  # Ensure compatibility with JPEG

            img.save(
                output_path,
                format="JPEG",
                quality=quality,
                optimize=True,
                exif=img.info.get("exif"),  # keep EXIF if available
            )

        if os.path.getsize(output_path) <= max_size_kb * 1024:
            break
        quality -= 5


# Function to compress PNGs and JPGs
def run(input_folder, output_folder, max_size_kb):
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            print(f"Processing: {filename}")
            input_path = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0] + ".jpg"  # force JPG output
            output_path = os.path.join(output_folder, output_filename)
            compress_image(input_path, output_path, max_size_kb)

            # Uncomment to remove original
            # os.remove(input_path)
            print(f"Saved compressed: {output_path}")


# Run the function on the provided folder
if __name__ == "__main__":
    run(input_dir, new_output_dir, max_size_kb)
