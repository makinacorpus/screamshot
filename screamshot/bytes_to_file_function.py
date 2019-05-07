"""
Bytes to png function
"""
from io import BytesIO

from PIL import Image


def bytes_to_file(b_img: bytes, path: str, img_format: str = None):
    """
    Transform the byte object representing an image into a file

    :param b_img: the image
    :type b_img: bytes

    :param path: the path to the future file
    :type path: str

    :param img_format: the type of the image file, \
        default value: type induced by path, or png if not found
    :type img_format: str
    """
    buffer = BytesIO(b_img)
    img = Image.open(buffer)
    img.save(path, format=img_format)
