import unittest

import pyppeteer

from screamshot.utils import get_browser, goto_page, to_sync


class GenerateBytesImgFunctionTests(unittest.TestCase):

    def setUp(self):
        self.browser = to_sync(get_browser())

    def test_goto_page_sync_basic(self):
        page1 = to_sync(goto_page(
            'http://localhost:5000/', self.browser))
        self.assertIsInstance(page1, pyppeteer.page.Page)

    def test_goto_page_sync_basic_same_page(self):
        page1 = to_sync(goto_page(
            'http://localhost:5000/index.html', self.browser))
        self.assertIsInstance(page1, pyppeteer.page.Page)
        page2 = to_sync(goto_page(
            'http://localhost:5000/index.html', self.browser))
        self.assertIsInstance(page2, pyppeteer.page.Page)
        self.assertEqual(page1, page2)

    def test_goto_page_sync_basic_different_page(self):
        page1 = to_sync(goto_page(
            'http://localhost:5000/index.html', self.browser))
        self.assertIsInstance(page1, pyppeteer.page.Page)
        page2 = to_sync(goto_page(
            'http://localhost:5000/other.html', self.browser))
        self.assertIsInstance(page2, pyppeteer.page.Page)
        self.assertNotEqual(page1, page2)

    def test_goto_page_sync_wait_until_incorrect(self):
        page = to_sync(goto_page(
            'http://localhost:5000/index.html', self.browser, wait_until='The end of the world'))
        self.assertNotIsInstance(page, pyppeteer.page.Page)

    def test_goto_page_sync_wait_until_domcontentloaded(self):
        page1 = to_sync(goto_page(
            'http://localhost:5000/index.html', self.browser))
        self.assertIsInstance(page1, pyppeteer.page.Page)
        page2 = to_sync(goto_page(
            'http://localhost:5000/index.html', self.browser, wait_until='domcontentloaded'))
        self.assertIsInstance(page2, pyppeteer.page.Page)
        self.assertNotEqual(page1, page2)

    def test_goto_page_sync_wait_until_networkidle0(self):
        page1 = to_sync(goto_page(
            'http://localhost:5000/index.html', self.browser))
        self.assertIsInstance(page1, pyppeteer.page.Page)
        page2 = to_sync(goto_page(
            'http://localhost:5000/index.html', self.browser, wait_until='networkidle0'))
        self.assertIsInstance(page2, pyppeteer.page.Page)
        self.assertNotEqual(page1, page2)

    def test_goto_page_sync_wait_until_load_and_domcontentloaded(self):
        page1 = to_sync(goto_page(
            'http://localhost:5000/index.html', self.browser))
        self.assertIsInstance(page1, pyppeteer.page.Page)
        page2 = to_sync(goto_page(
            'http://localhost:5000/index.html', self.browser,
            wait_until=['load', 'domcontentloaded']))
        self.assertIsInstance(page2, pyppeteer.page.Page)
        self.assertNotEqual(page1, page2)

    def test_goto_page_sync_wait_for(self):
        page = to_sync(goto_page(
            'http://localhost:5000/other.html', self.browser, wait_for='#godot'))
        self.assertIsInstance(page, pyppeteer.page.Page)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
