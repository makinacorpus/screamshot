import unittest

from screamshot import generate_bytes_img


class GenerateBytesImgFunctionTests(unittest.TestCase):

    def test_bad_url(self):
        with self.assertRaisesRegex(AssertionError, 'url parameter must be a string'):
            generate_bytes_img(1)

    def test_height_without_width(self):
        with self.assertRaisesRegex(AssertionError,
                                    'both height and width must be define or none of them'):
            generate_bytes_img('https://www.google.fr', width=3)

    def test_width_without_height(self):
        with self.assertRaisesRegex(AssertionError,
                                    'both height and width must be define or none of them'):
            generate_bytes_img('https://www.google.fr', height=3)

    def test_bad_type_width(self):
        with self.assertRaisesRegex(AssertionError,
                                    'width must be a positive integer'):
            generate_bytes_img('https://www.google.fr', width='b', height=3)

    def test_bad_width(self):
        with self.assertRaisesRegex(AssertionError,
                                    'width must be a positive integer'):
            generate_bytes_img('https://www.google.fr', width=-8, height=3)

    def test_bad_type_height(self):
        with self.assertRaisesRegex(AssertionError,
                                    'height must be a positive integer'):
            generate_bytes_img('https://www.google.fr', height='b', width=3)

    def test_bad_height(self):
        with self.assertRaisesRegex(AssertionError,
                                    'height must be a positive integer'):
            generate_bytes_img('https://www.google.fr', height=-8, width=3)

    def test_bad_selector(self):
        with self.assertRaisesRegex(AssertionError,
                                    'selector must be a string'):
            generate_bytes_img('https://www.google.fr', selector=1)

    def test_bad_wait_for(self):
        with self.assertRaisesRegex(AssertionError,
                                    'wait_for must be a string'):
            generate_bytes_img('https://www.google.fr', wait_for=1)

    def test_bad_type_wait_until(self):
        with self.assertRaisesRegex(AssertionError,
                                    'wait_until should be a string or a list of string of load, '
                                    + 'domcontentloaded, networkidle0 or networkidle2'):
            generate_bytes_img('https://www.google.fr', wait_until=1)

    def test_bad_param_wait_until(self):
        with self.assertRaisesRegex(AssertionError,
                                    'wait_until should be a string or a list of string of load, '
                                    + 'domcontentloaded, networkidle0 or networkidle2'):
            generate_bytes_img('https://www.google.fr', wait_until='b')

    def test_without_kwargs(self):
        img = generate_bytes_img('https://www.google.fr')
        self.assertTrue(isinstance(img, bytes))

    def test_selector(self):
        img = generate_bytes_img('https://makina-corpus.com/expertise/cartographie',
                                 selector='.image-right')
        self.assertTrue(isinstance(img, bytes))

    def test_wait_for(self):
        img = generate_bytes_img('https://makina-corpus.com/expertise/cartographie',
                                 wait_for='.image-right')
        self.assertTrue(isinstance(img, bytes))

    def test_arg_viewport(self):
        img = generate_bytes_img('https://makina-corpus.com/expertise/cartographie',
                                 width=800, height=600)
        self.assertTrue(isinstance(img, bytes))

    def test_wait_until(self):
        img = generate_bytes_img('https://makina-corpus.com/expertise/cartographie',
                                 wait_until='networkidle0')
        self.assertTrue(isinstance(img, bytes))

if __name__ == '__main__':
    unittest.main()
