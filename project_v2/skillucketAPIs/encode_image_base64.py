""" Checking if an image is valid and if yes, converting it to a string in base64 """
import base64
import PIL
from PIL import Image


def is_image_valid(image_path):
    """checking if the file exists and is actually an image, always returning a boolean"""

    try:
        image = Image.open(image_path)
        image.close()
        return True
    except FileNotFoundError:
        return False
    except PIL.UnidentifiedImageError:
        return False


def encode_image_base64(image_path):
    """encode an image file into base64 and return the string"""

    if is_image_valid(image_path):
        with open(image_path, mode="rb") as image_file:
            image_bytes = image_file.read()
            encoded_image = base64.b64encode(image_bytes)
        return encoded_image
    return "An invalid or non-existent file. Please upload an image."
