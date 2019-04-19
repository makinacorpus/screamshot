# import os
import unittest
# import asyncio

import pyppeteer

from screamshot.utils import get_browser_sync, goto_page_sync, to_sync
# from screamshot import generate_bytes_img, generate_bytes_img_prom


class GenerateBytesImgFunctionTests(unittest.TestCase):

    def setUp(self):
        self.browser = get_browser_sync(
            is_headless=False, write_websocket=True)

    def test_goto_page_sync_basic(self):
        page = goto_page_sync(
            'http://0.0.0.0:8000/', self.browser)
        self.assertIsInstance(page, pyppeteer.page.Page)

    def test_goto_page_sync_basic_same_page(self):
        page1 = goto_page_sync(
            'http://0.0.0.0:8000/website_test/', self.browser)
        self.assertIsInstance(page1, pyppeteer.page.Page)

        page2 = goto_page_sync(
            'http://0.0.0.0:8000/website_test/', self.browser)
        self.assertIsInstance(page2, pyppeteer.page.Page)

        self.assertEqual(page1, page2)
        to_sync(page1.close())

    def test_goto_page_sync_basic_different_page(self):
        page1 = goto_page_sync(
            'http://0.0.0.0:8000/website_test/', self.browser)
        self.assertIsInstance(page1, pyppeteer.page.Page)

        page2 = goto_page_sync(
            'http://0.0.0.0:8000/website_test/other.html', self.browser)
        self.assertIsInstance(page2, pyppeteer.page.Page)

        self.assertNotEqual(page1, page2)
        to_sync(page1.close())
        to_sync(page2.close())

    def test_goto_page_sync_wait_until_incorrect(self):
        page = goto_page_sync(
            'http://0.0.0.0:8000/website_test/', self.browser, wait_until='The end of the world')
        self.assertNotIsInstance(page, pyppeteer.page.Page)

    def test_goto_page_sync_wait_until_domcontentloaded(self):
        page1 = goto_page_sync(
            'http://0.0.0.0:8000/website_test/', self.browser)
        self.assertIsInstance(page1, pyppeteer.page.Page)

        page2 = goto_page_sync(
            'http://0.0.0.0:8000/website_test/', self.browser, wait_until='domcontentloaded')
        self.assertIsInstance(page2, pyppeteer.page.Page)

        self.assertNotEqual(page1, page2)
        to_sync(page1.close())
        to_sync(page2.close())

    def test_goto_page_sync_wait_until_networkidle0(self):
        page1 = goto_page_sync(
            'http://0.0.0.0:8000/website_test/', self.browser)
        self.assertIsInstance(page1, pyppeteer.page.Page)

        page2 = goto_page_sync(
            'http://0.0.0.0:8000/website_test/', self.browser, wait_until='networkidle0')
        self.assertIsInstance(page2, pyppeteer.page.Page)

        self.assertNotEqual(page1, page2)
        to_sync(page1.close())
        to_sync(page2.close())

    def test_goto_page_sync_wait_until_load_and_domcontentloaded(self):
        page1 = goto_page_sync(
            'http://0.0.0.0:8000/website_test/', self.browser)
        self.assertIsInstance(page1, pyppeteer.page.Page)

        page2 = goto_page_sync(
            'http://0.0.0.0:8000/website_test/', self.browser, wait_until=['load', 'domcontentloaded'])
        self.assertIsInstance(page2, pyppeteer.page.Page)

        self.assertNotEqual(page1, page2)
        to_sync(page1.close())
        to_sync(page2.close())

    def test_goto_page_sync_wait_for(self):
        page = goto_page_sync(
            'http://0.0.0.0:8000/website_test/', self.browser, wait_for='#godot', wait_until='domcontentloaded')
        self.assertIsInstance(page, pyppeteer.page.Page)

    # def test_function_without_promise_without_optional_parameters(self):
    #     img = asyncio.get_event_loop().run_until_complete(
    #         generate_bytes_img('http://0.0.0.0:8000/website_test/')
    #     )
    #     self.assertTrue(img and isinstance(img, bytes))

    # def test_function_with_promise_without_optional_parameters(self):
    #     loop = asyncio.get_event_loop()
    #     future = asyncio.Future()
    #     asyncio.ensure_future(
    #         generate_bytes_img_prom('http://0.0.0.0:8000/website_test/', future))
    #     loop.run_until_complete(future)
    #     img = future.result()
    #     self.assertTrue(img and isinstance(img, bytes))

    def tearDown(self):
        pass
        # to_sync(self.browser.close())


if __name__ == '__main__':
    unittest.main()
