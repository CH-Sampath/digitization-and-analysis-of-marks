import os

from PIL import Image

def modify_image(image_path, output_path, new_size, dpi):
    # Open an image file
    with Image.open(image_path) as img:
        # Resize image
        img = img.resize(new_size, Image.LANCZOS, resample=Image.NEAREST)
        # Save image with new DPI
        img.save(output_path, dpi=dpi)

def mod_img(in_path, out_path, new_size, dpi):

    for f in os.listdir(in_path):
        old_path = os.path.join(in_path, f)
        with Image.open(old_path) as img:
            # Resize image
            img = img.resize(new_size, resample=Image.NEAREST)
            # Save image with new DPI
            new_image = os.path.join(out_path, f)
            img.save(new_image, dpi=dpi)

# Usage
mod_img('C:\\major-version1.0\\dataset - 1100px', 'C:\\major-version1.0\\resizedto1400', (1430, 822), (200, 200))
