# import os
import unittest
# import asyncio
from os import system

import pyppeteer

from screamshot.utils import get_browser_sync, goto_page_sync, to_sync
# from screamshot import generate_bytes_img, generate_bytes_img_prom


class GenerateBytesImgFunctionTests(unittest.TestCase):

    def setUp(self):
        self.browser = get_browser_sync(
            is_headless=False, write_websocket=True)

    def test_goto_page_sync_basic(self):
        self.page1 = goto_page_sync(
            'http://server:5000/', self.browser)
        self.assertIsInstance(self.page1, pyppeteer.page.Page)

    def test_goto_page_sync_basic_same_page(self):
        self.page1 = goto_page_sync(
            'http://server:5000/index.html', self.browser)
        self.assertIsInstance(self.page1, pyppeteer.page.Page)
        self.page2 = goto_page_sync(
            'http://server:5000/index.html', self.browser)
        self.assertIsInstance(self.page2, pyppeteer.page.Page)
        self.assertEqual(self.page1, self.page2)

    def test_goto_page_sync_basic_different_page(self):
        self.page1 = goto_page_sync(
            'http://server:5000/index.html', self.browser)
        self.assertIsInstance(self.page1, pyppeteer.page.Page)
        self.page2 = goto_page_sync(
            'http://server:5000/other.html', self.browser)
        self.assertIsInstance(self.page2, pyppeteer.page.Page)
        self.assertNotEqual(self.page1, self.page2)

    def test_goto_page_sync_wait_until_incorrect(self):
        page = goto_page_sync(
            'http://server:5000/index.html', self.browser, wait_until='The end of the world')
        self.assertNotIsInstance(page, pyppeteer.page.Page)

    def test_goto_page_sync_wait_until_domcontentloaded(self):
        self.page1 = goto_page_sync(
            'http://server:5000/index.html', self.browser)
        self.assertIsInstance(self.page1, pyppeteer.page.Page)
        self.page2 = goto_page_sync(
            'http://server:5000/index.html', self.browser, wait_until='domcontentloaded')
        self.assertIsInstance(self.page2, pyppeteer.page.Page)
        self.assertNotEqual(self.page1, self.page2)

    def test_goto_page_sync_wait_until_networkidle0(self):
        self.page1 = goto_page_sync(
            'http://server:5000/index.html', self.browser)
        self.assertIsInstance(self.page1, pyppeteer.page.Page)
        self.page2 = goto_page_sync(
            'http://server:5000/index.html', self.browser, wait_until='networkidle0')
        self.assertIsInstance(self.page2, pyppeteer.page.Page)
        self.assertNotEqual(self.page1, self.page2)

    def test_goto_page_sync_wait_until_load_and_domcontentloaded(self):
        self.page1 = goto_page_sync(
            'http://server:5000/index.html', self.browser)
        self.assertIsInstance(self.page1, pyppeteer.page.Page)
        self.page2 = goto_page_sync(
            'http://server:5000/index.html', self.browser, wait_until=['load', 'domcontentloaded'])
        self.assertIsInstance(self.page2, pyppeteer.page.Page)
        self.assertNotEqual(self.page1, self.page2)

    def test_goto_page_sync_wait_for(self):
        page = goto_page_sync(
            'http://server:5000/other.html', self.browser, wait_for='#godot', wait_until='domcontentloaded')
        self.assertIsInstance(page, pyppeteer.page.Page)

    def tearDown(self):
        try:
            to_sync(self.page1.close())
        except:
            pass
        try:
            to_sync(self.page2.close())
        except:
            pass


if __name__ == '__main__':
    unittest.main()
