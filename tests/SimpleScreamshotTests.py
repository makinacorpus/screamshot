import unittest

from screamshot import ScreenShot


class SimpleScreamshotTests(unittest.TestCase):
    def setUp(self):
        self.screenShot = ScreenShot('https://www.google.fr')

    def test_works(self):
        img = self.screenShot.take()
        self.assertTrue(isinstance(img, bytes))


if __name__ == '__main__':
    unittest.main()
