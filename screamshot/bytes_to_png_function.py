"""
Bytes to png function
"""
from io import BytesIO

from PIL import Image


def bytes_to_png(b_img: bytes, path: str):
    """
    Transform the byte object representing an image into a png file

    :param b_img: the image
    :type b_img: bytes

    :param path: the path to the future png file
    :type path: str
    """
    buffer = BytesIO(b_img)
    img = Image.open(buffer)
    img.save(path)
