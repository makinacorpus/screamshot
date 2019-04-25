"""
Tests `utils.py` functions
"""
import unittest

import pyppeteer
from pyppeteer.browser import Browser

from screamshot.utils import get_browser, close_browser, goto_page, to_sync
# from screamshot import generate_bytes_img, generate_bytes_img_prom


class TestsUtilsFunctions(unittest.TestCase):
    """
    Tests `utils.py` functions
    """
    def setUp(self):
        self.browser = to_sync(get_browser(launch_args=['--no-sandbox']))

    def test_goto_page_basic(self):
        """
        Tests `goto_page` without optionnal parameter
        """
        page1 = to_sync(goto_page(
            'http://127.0.0.1:5000/', self.browser))
        self.assertIsInstance(page1, pyppeteer.page.Page)

    def test_goto_page_basic_same_page(self):
        """
        Generates a page twice with `goto_page` and checks if they are equal
        """
        page1 = to_sync(goto_page(
            'http://127.0.0.1:5000/index.html', self.browser))
        self.assertIsInstance(page1, pyppeteer.page.Page)
        page2 = to_sync(goto_page(
            'http://127.0.0.1:5000/index.html', self.browser))
        self.assertIsInstance(page2, pyppeteer.page.Page)
        self.assertEqual(page1, page2)

    def test_goto_page_basic_different_page(self):
        """
        Generates two different pages and checks if they are different
        """
        page1 = to_sync(goto_page(
            'http://127.0.0.1:5000/index.html', self.browser))
        self.assertIsInstance(page1, pyppeteer.page.Page)
        page2 = to_sync(goto_page(
            'http://127.0.0.1:5000/other.html', self.browser))
        self.assertIsInstance(page2, pyppeteer.page.Page)
        self.assertNotEqual(page1, page2)

    def test_goto_page_wait_until_incorrect(self):
        """
        Gives a bad optional `wait_until` parameter and checks that the result is not a page
        """
        page = to_sync(goto_page(
            'http://127.0.0.1:5000/index.html', self.browser, wait_until='The end of the world'))
        self.assertNotIsInstance(page, pyppeteer.page.Page)

    def test_goto_page_wait_until_domcontentloaded(self):
        """
        Tests that *domcontentloaded* `wait_until` parameter works
        """
        page1 = to_sync(goto_page(
            'http://127.0.0.1:5000/index.html', self.browser))
        self.assertIsInstance(page1, pyppeteer.page.Page)
        page2 = to_sync(goto_page(
            'http://127.0.0.1:5000/index.html', self.browser, wait_until='domcontentloaded'))
        self.assertIsInstance(page2, pyppeteer.page.Page)
        self.assertNotEqual(page1, page2)

    def test_goto_page_wait_until_networkidle0(self):
        """
        Tests that *networkidle0* `wait_until` parameter works
        """
        page1 = to_sync(goto_page(
            'http://127.0.0.1:5000/index.html', self.browser))
        self.assertIsInstance(page1, pyppeteer.page.Page)
        page2 = to_sync(goto_page(
            'http://127.0.0.1:5000/index.html', self.browser, wait_until='networkidle0'))
        self.assertIsInstance(page2, pyppeteer.page.Page)
        self.assertNotEqual(page1, page2)

    def test_goto_page_wait_for(self):
        """
        Tests that `wait_for` works
        """
        page = to_sync(goto_page(
            'http://127.0.0.1:5000/other.html', self.browser, wait_for='#godot',
            wait_until='domcontentloaded'))
        self.assertIsInstance(page, pyppeteer.page.Page)

    def test_get_browser(self):
        browser = to_sync(get_browser())
        self.assertIsInstance(browser, Browser)

    def tearDown(self):
        to_sync(close_browser())


if __name__ == '__main__':
    unittest.main()
