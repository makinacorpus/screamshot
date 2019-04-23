import unittest

from os import remove
from os.path import exists

from io import BytesIO

import numpy as np

from PIL import Image


from screamshot import generate_bytes_img
from screamshot.utils import to_sync


def rmsd(img1, img2):
    img1 = (img1 - np.mean(img1)) / (np.std(img1))
    img2 = (img2 - np.mean(img2)) / (np.std(img2))
    return np.sqrt(np.mean((img1-img2)**2))


# Usefull for basic tests
def is_same_image(img1, img2):
    return (img1.size == img2.size) and (abs(rmsd(img1, img2)) < 0.05)


class GenerateBytesImgFunctionTests(unittest.TestCase):

    def setUp(self):
        self.img_dog = Image.open('tests/server/static/OtherPage/aww_dog.jpg')
        self.img_dog_change = Image.open(
            'tests/server/static/OtherPage/aww_dog_change.jpg')
        self.img_kitten = Image.open(
            'tests/server/static/OtherPage/aww_kitten.jpg')

    def test_screamshot_same_bytes_write(self):
        img_bytes = BytesIO(to_sync(generate_bytes_img(
            url='http://localhost:5000/other.html',
            path='test_img.jpg',
            selector='#godot')))   # Use of path to specify the type
        img_bytes = Image.open(img_bytes)
        img_file = Image.open('test_img.jpg')

        self.assertTupleEqual(img_bytes.size, img_file.size)
        self.assertAlmostEqual(rmsd(img_bytes, img_file), 0, delta=0.05)

    def test_screamshot_same_dog(self):
        to_sync(generate_bytes_img(
            url='http://localhost:5000/other.html',
            selector='#godot',
            path='test_img.jpg'))
        img = Image.open('test_img.jpg')

        self.assertTrue(is_same_image(img, self.img_dog))

    def test_screamshot_same_kitten(self):
        to_sync(generate_bytes_img(
            url='http://localhost:5000/other.html',
            selector='#caterpillar',
            path='test_img.jpg'))
        img = Image.open('test_img.jpg')

        self.assertTrue(is_same_image(img, self.img_kitten))

    def test_screamshot_different_image(self):
        to_sync(generate_bytes_img(
            url='http://localhost:5000/other.html',
            selector='#godot',
            path='test_img.jpg'))
        img = Image.open('test_img.jpg')

        self.assertEqual(img.size, self.img_dog.size)
        self.assertNotAlmostEqual(
            rmsd(img, self.img_dog_change), 0, delta=0.05)

    def test_screamshot_different_size(self):
        to_sync(generate_bytes_img(
            url='http://localhost:5000/other.html',
            selector='#godot',
            path='test_img.jpg'))
        img = Image.open('test_img.jpg')

        self.assertNotEqual(img.size, self.img_kitten.size)

    def tearDown(self):
        if exists('test_img.jpg'):
            remove('test_img.jpg')


if __name__ == '__main__':
    unittest.main()
