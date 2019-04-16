import os
import unittest
import asyncio

from pyppeteer import launch

from screamshot import generate_bytes_img, generate_bytes_img_prom


class GenerateBytesImgFunctionTests(unittest.TestCase):

    def setUp(self):
        self.browser = asyncio.get_event_loop().run_until_complete(
            launch(headless=True, onClose=False))
        os.environ['WS_ENDPOINT_SCREAMSHOT'] = self.browser.wsEndpoint

    def test_function_without_promise_without_optional_parameters(self):
        img = asyncio.get_event_loop().run_until_complete(
            generate_bytes_img('https://www.google.fr')
        )
        self.assertTrue(img and isinstance(img, bytes))

    def test_function_with_promise_without_optional_parameters(self):
        loop = asyncio.get_event_loop()
        future = asyncio.Future()
        asyncio.ensure_future(
            generate_bytes_img_prom('https://www.google.fr', future))
        loop.run_until_complete(future)
        img = future.result()
        self.assertTrue(img and isinstance(img, bytes))

    def tearDown(self):
        asyncio.get_event_loop().run_until_complete(
            self.browser.close())


if __name__ == '__main__':
    unittest.main()
