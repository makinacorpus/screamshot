"""
Tests browser manager script
"""
from unittest import TestCase, main
from subprocess import run

from pyppeteer import connect
from pyppeteer.browser import Browser

from screamshot.utils import to_sync, get_endpoint


class TestBrowserManagerScript(TestCase):
    """
    Test class
    """
    def test_open_headless_browser(self):
        """
        Opens a headless browser, checks if it is open and closes it
        """
        run(['python3', 'screamshot/browser_manager_script.py', '-o', '-ns'])
        endpoint = get_endpoint()
        browser = to_sync(connect({'browserWSEndpoint': endpoint}))
        self.assertIsInstance(browser, Browser)
        run(['python3', 'screamshot/browser_manager_script.py', '-c'])


if __name__ == '__main__':
    main()
