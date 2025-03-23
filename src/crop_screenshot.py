import sys
from pathlib import Path

from PIL import Image


def crop_top_left_quadrant(input_path, output_path):
    # Open the original image
    with Image.open(input_path) as img:
        # Get the image dimensions
        width, height = img.size
        print(f"Original size: {width}x{height}")

        # Calculate half of width and height
        half_width = width // 2
        half_height = height // 2

        # Define the box to crop (left, upper, right, lower)
        crop_box = (0, 0, half_width, half_height)

        # Crop the image
        cropped_img = img.crop(crop_box)

        # Save the cropped image
        cropped_img.save(output_path)
        print(f"Cropped image saved to {output_path}")


input_fpath = Path(sys.argv[1])
assert input_fpath.is_file()
output_fpath = input_fpath.parent.joinpath(input_fpath.stem + '_crop' + input_fpath.suffix)
crop_top_left_quadrant(input_fpath, output_fpath)
