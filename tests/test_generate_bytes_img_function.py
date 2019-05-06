"""
Tests the generate_bytes_img functions on a local server
"""
import asyncio
import unittest
from os import remove
from os.path import exists
from io import BytesIO

import numpy as np

from PIL import Image

from screamshot import (
    generate_bytes_img,
    generate_bytes_img_prom,
    generate_bytes_img_django_wrap,
)
from screamshot.utils import to_sync, get_browser, close_browser


TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoibWFraW5hIn0.\
jUTxi6c2-o3nHJ6Bq7zRXFoKixUyYetgPX3cToOayiA"


def _rmsd(img1, img2):
    img1 = (img1 - np.mean(img1)) / (np.std(img1))
    img2 = (img2 - np.mean(img2)) / (np.std(img2))
    return np.sqrt(np.mean((img1 - img2) ** 2))


# Usefull for basic tests
def _is_same_image(img1, img2):
    return (img1.size == img2.size) and (abs(_rmsd(img1, img2)) < 0.05)


class TestGenerateBytesImgFunction(unittest.TestCase):
    """
    Test class
    """

    def setUp(self):
        to_sync(get_browser(launch_args=["--no-sandbox"]))

        self.img_dog = Image.open("tests/server/static/images/aww_dog.jpg")
        self.img_dog_change = Image.open(
            "tests/server/static/images/aww_dog_change.jpg"
        )
        self.img_kitten = Image.open("tests/server/static/images/aww_kitten.jpg")

    def test_screenshot_protected_page_no_auth(self):
        with self.assertRaisesRegex(
            AttributeError, "'NoneType' object has no attribute 'screenshot'"
        ):
            to_sync(
                generate_bytes_img(
                    "http://localhost:5000/protected_index", selector="#godot"
                )
            )

    def test_screenshot_protected_page_bad_auth(self):
        with self.assertRaisesRegex(
            AttributeError, "'NoneType' object has no attribute 'screenshot'"
        ):
            to_sync(
                generate_bytes_img(
                    "http://localhost:5000/protected_index",
                    selector="#godot",
                    credentials={"token_in_header": True, "token": "xxx"},
                )
            )
        with self.assertRaisesRegex(
            AttributeError, "'NoneType' object has no attribute 'screenshot'"
        ):
            to_sync(
                generate_bytes_img(
                    "http://localhost:5000/protected_index",
                    selector="#godot",
                    credentials={"token": TOKEN},
                )
            )

    def test_screenshot_protected_page_with_auth_token(self):
        img_bytes = BytesIO(
            to_sync(
                generate_bytes_img(
                    "http://localhost:5000/protected_index",
                    selector="#godot",
                    credentials={"token_in_header": True, "token": TOKEN},
                )
            )
        )
        img = Image.open(img_bytes)
        dog_img = Image.open("tests/server/static/images/aww_dog.jpg").convert("RGBA")
        kitten_img = Image.open("tests/server/static/images/aww_kitten.jpg").convert(
            "RGBA"
        )
        self.assertTrue(_is_same_image(img, dog_img))
        self.assertFalse(_is_same_image(img, kitten_img))

    def test_screenshot_protected_page_with_auth_login(self):
        img_bytes = BytesIO(
            to_sync(
                generate_bytes_img(
                    "http://localhost:5000/protected_index",
                    selector="#godot",
                    credentials={"username": "makina", "password": "makina"},
                )
            )
        )
        img = Image.open(img_bytes)
        dog_img = Image.open("tests/server/static/images/aww_dog.jpg").convert("RGBA")
        kitten_img = Image.open("tests/server/static/images/aww_kitten.jpg").convert(
            "RGBA"
        )
        self.assertTrue(_is_same_image(img, dog_img))
        self.assertFalse(_is_same_image(img, kitten_img))

    def test_screamshot_same_bytes_write(self):
        """
        Takes a screenshot and compares the buffer to the saved image.
        """
        img_bytes = BytesIO(
            to_sync(
                generate_bytes_img(
                    "http://localhost:5000/index.html",
                    path="test_img.jpg",  # Use of path to specify the type
                    selector="#godot",
                )
            )
        )
        img_bytes = Image.open(img_bytes)
        img_file = Image.open("test_img.jpg")

        self.assertTupleEqual(img_bytes.size, img_file.size)
        self.assertAlmostEqual(_rmsd(img_bytes, img_file), 0, delta=0.05)

    def test_screamshot_same_dog(self):
        """
        Takes a screenshot of a given div and compares it to the real image.
        """
        to_sync(
            generate_bytes_img(
                "http://localhost:5000/index.html",
                selector="#godot",
                path="test_img.jpg",
            )
        )
        img = Image.open("test_img.jpg")

        self.assertTrue(_is_same_image(img, self.img_dog))

    def test_screamshot_same_kitten(self):
        """
        Takes a screenshot of a given div and compares it to the real image.
        """
        to_sync(
            generate_bytes_img(
                "http://localhost:5000/index.html",
                selector="#caterpillar",
                path="test_img.jpg",
            )
        )
        img = Image.open("test_img.jpg")

        self.assertTrue(_is_same_image(img, self.img_kitten))

    def test_screamshot_different_image(self):
        """
        Takes a screenshot of a given div and compares it to a different image.
        """
        to_sync(
            generate_bytes_img(
                "http://localhost:5000/index.html",
                selector="#godot",
                path="test_img.jpg",
            )
        )
        img = Image.open("test_img.jpg")

        self.assertEqual(img.size, self.img_dog.size)
        self.assertNotAlmostEqual(_rmsd(img, self.img_dog_change), 0, delta=0.05)

    def test_screamshot_same_bytes_write_with_promise(self):
        """
        Takes a screenshot and compares the buffer to the saved image.
        Uses a promise.
        """
        loop = asyncio.get_event_loop()
        future = asyncio.Future()
        asyncio.ensure_future(
            generate_bytes_img_prom(
                "http://localhost:5000/index.html",
                future,
                selector="#godot",
                path="test_img.jpg",
            )
        )
        loop.run_until_complete(future)
        img_bytes = BytesIO(future.result())  # Use of path to specify the type
        img_bytes = Image.open(img_bytes)
        img_file = Image.open("test_img.jpg")

        self.assertTupleEqual(img_bytes.size, img_file.size)
        self.assertAlmostEqual(_rmsd(img_bytes, img_file), 0, delta=0.05)

    def test_screamshot_same_dog_with_promise(self):
        """
        Takes a screenshot of a given div and compares it to the real image.
        Uses a promise.
        """
        loop = asyncio.get_event_loop()
        future = asyncio.Future()
        asyncio.ensure_future(
            generate_bytes_img_prom(
                "http://localhost:5000/index.html",
                future,
                selector="#godot",
                path="test_img.jpg",
            )
        )
        loop.run_until_complete(future)
        img = Image.open("test_img.jpg")

        self.assertTrue(_is_same_image(img, self.img_dog))

    def test_screamshot_same_kitten_with_promise(self):
        """
        Takes a screenshot of a given div and compares it to the real image.
        Uses a promise.
        """
        loop = asyncio.get_event_loop()
        future = asyncio.Future()
        asyncio.ensure_future(
            generate_bytes_img_prom(
                "http://localhost:5000/index.html",
                future,
                selector="#caterpillar",
                path="test_img.jpg",
            )
        )
        loop.run_until_complete(future)
        img = Image.open("test_img.jpg")

        self.assertTrue(_is_same_image(img, self.img_kitten))

    def test_screamshot_different_image_with_promise(self):
        """
        Takes a screenshot of a given div and compares it to a different image.
        Uses promise.
        """
        loop = asyncio.get_event_loop()
        future = asyncio.Future()
        asyncio.ensure_future(
            generate_bytes_img_prom(
                "http://localhost:5000/index.html",
                future,
                selector="#godot",
                path="test_img.jpg",
            )
        )
        loop.run_until_complete(future)
        img = Image.open("test_img.jpg")

        self.assertEqual(img.size, self.img_dog.size)
        self.assertNotAlmostEqual(_rmsd(img, self.img_dog_change), 0, delta=0.05)

    def test_screamshot_same_bytes_write_with_django_wrap(self):
        """
        Takes a screenshot and compares the buffer to the saved image.
        Uses the django_wrap function.
        """
        img_bytes = generate_bytes_img_django_wrap(
            "http://localhost:5000/index.html",
            selector="#godot",
            path="test_img.jpg",  # Use of path to specify the type
        )
        img_bytes = BytesIO(img_bytes)
        img_bytes = Image.open(img_bytes)
        img_file = Image.open("test_img.jpg")

        self.assertTupleEqual(img_bytes.size, img_file.size)
        self.assertAlmostEqual(_rmsd(img_bytes, img_file), 0, delta=0.05)

    def test_screamshot_same_dog_with_django_wrap(self):
        """
        Takes a screenshot of a given div and compares it to the real image.
        Uses the django_wrap function.
        """
        generate_bytes_img_django_wrap(
            "http://localhost:5000/index.html", selector="#godot", path="test_img.jpg"
        )
        img = Image.open("test_img.jpg")

        self.assertTrue(_is_same_image(img, self.img_dog))

    def test_screamshot_same_kitten_with_django_wrap(self):
        """
        Takes a screenshot of a given div and compares it to the real image.
        Uses the django_wrap function.
        """
        generate_bytes_img_django_wrap(
            "http://localhost:5000/index.html",
            selector="#caterpillar",
            path="test_img.jpg",
        )
        img = Image.open("test_img.jpg")

        self.assertTrue(_is_same_image(img, self.img_kitten))

    def test_screamshot_different_image_with_django_wrap(self):
        """
        Takes a screenshot of a given div and compares it to a different image.
        Uses the django_wrap function.
        """
        generate_bytes_img_django_wrap(
            "http://localhost:5000/index.html", selector="#godot", path="test_img.jpg"
        )
        img = Image.open("test_img.jpg")

        self.assertEqual(img.size, self.img_dog.size)
        self.assertNotAlmostEqual(_rmsd(img, self.img_dog_change), 0, delta=0.05)

    def tearDown(self):
        to_sync(close_browser())

        if exists("test_img.jpg"):
            remove("test_img.jpg")
