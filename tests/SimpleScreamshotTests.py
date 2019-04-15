import unittest

from screamshot import ScreenShot


class SimpleScreamshotTests(unittest.TestCase):
    def setUp(self):
        self.base = ScreenShot('https://www.google.fr')

    def test_base(self):
        img = self.base.load_and_screamshot()
        self.assertTrue(isinstance(img, bytes))

    def test_bad_url(self):
        with self.assertRaises(AssertionError):
            ScreenShot(1)

if __name__ == '__main__':
    unittest.main()
