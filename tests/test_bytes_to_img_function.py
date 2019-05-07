from os import remove
from io import BytesIO
from unittest import TestCase

from PIL import Image

import numpy as np

from screamshot.bytes_to_file_function import bytes_to_file


def _rmsd(img1, img2):
    img1 = (img1 - np.mean(img1)) / (np.std(img1))
    img2 = (img2 - np.mean(img2)) / (np.std(img2))
    return np.sqrt(np.mean((img1 - img2) ** 2))


# Usefull for basic tests
def _is_same_image(img1, img2):
    return (img1.size == img2.size) and (abs(_rmsd(img1, img2)) < 0.05)


class TestBytesToImgFunction(TestCase):
    def test_bytes_to_img(self):
        img = Image.open("tests/server/static/images/aww_dog.jpg")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        b_img = buffer.getvalue()
        self.assertIsInstance(b_img, bytes)
        bytes_to_file(b_img, "basic_bytes_to_img_test.png")

        # Test if the file exists
        saved_img = Image.open("basic_bytes_to_img_test.png")
        self.assertTrue(_is_same_image(img, saved_img))
        remove("basic_bytes_to_img_test.png")
