"""
Unit tests of `generate_bytes_img_function.py`
"""
from unittest import TestCase
from unittest.mock import patch
from asyncio import get_event_loop, Future, ensure_future

from screamshot.generate_bytes_img_functions import (
    _parse_parameters,
    _page_manager,
    _selector_manager,
    generate_bytes_img,
    generate_bytes_img_prom,
)
from screamshot.utils import to_sync


class FakePage:
    def __init__(
        self,
        arg_viewport=None,
        wait_until=None,
        goto_called=False,
        url=None,
        waitForSelector_called=False,
        wait_for=None,
        waitForxPath_called=False,
        wait_for_xpath=None,
        querySelector_called=False,
        selector=None,
        credentials=None,
        credentials_token_request=None,
        use_local_token=None,
    ):
        self.arg_viewport = arg_viewport
        self.credentials = credentials
        self.credentials_token_request = credentials_token_request
        self.wait_until = wait_until
        self.goto_called = goto_called
        self.url = url
        self.waitForSelector_called = waitForSelector_called
        self.wait_for = wait_for
        self.waitForxPath_called = waitForxPath_called
        self.wait_for_xpath = wait_for_xpath
        self.querySelector_called = querySelector_called
        self.selector = selector
        if use_local_token:
            self.credentials_token_request = {"token": "xxx"}

    async def setViewport(self, arg_viewport):
        self.arg_viewport = arg_viewport

    async def authenticate(self, credentials):
        self.credentials = credentials

    async def setExtraHTTPHeaders(self, credentials):
        self.credentials = credentials

    async def goto(self, url, waitUntil=None):
        self.goto_called = True
        self.url = url
        self.wait_until = waitUntil

    async def waitForSelector(self, wait_for):
        self.waitForSelector_called = True
        self.wait_for = wait_for

    async def waitForXPath(self, wait_for_xpath):
        self.waitForxPath_called = True
        self.wait_for_xpath = wait_for_xpath

    async def querySelector(self, selector):
        self.querySelector_called = True
        self.selector = selector
        return self

    async def screenshot(self, **kwargs):
        return "screenshot !"

    async def close(self):
        pass


class FakeBrowser:
    async def newPage(self):
        return FakePage()


async def get_browser():
    return FakeBrowser()


class TestGenerateBytesImgFunctionUnit(TestCase):
    """
    Test class
    """

    def test_parse_parameters(self):
        """
        Tests _parse_parameters
        """
        self.assertEqual(
            _parse_parameters(),
            {
                "arg_viewport": {},
                "screenshot_options": {"fullPage": False},
                "selector": None,
                "wait_for": None,
                "wait_for_xpath": None,
                "wait_until": ["load"],
                "credentials": {},
                "credentials_token_request": {},
                "use_local_token": None,
            },
        )
        self.assertEqual(
            _parse_parameters(width=800),
            {
                "arg_viewport": {"width": 800},
                "screenshot_options": {"fullPage": False},
                "selector": None,
                "wait_for": None,
                "wait_for_xpath": None,
                "wait_until": ["load"],
                "credentials": {},
                "credentials_token_request": {},
                "use_local_token": None,
            },
        )
        self.assertEqual(
            _parse_parameters(height=800),
            {
                "arg_viewport": {"height": 800},
                "screenshot_options": {"fullPage": False},
                "selector": None,
                "wait_for": None,
                "wait_for_xpath": None,
                "wait_until": ["load"],
                "credentials": {},
                "credentials_token_request": {},
                "use_local_token": None,
            },
        )
        self.assertEqual(
            _parse_parameters(wait_until=["networkidle0"]),
            {
                "arg_viewport": {},
                "screenshot_options": {"fullPage": False},
                "selector": None,
                "wait_for": None,
                "wait_for_xpath": None,
                "wait_until": ["networkidle0"],
                "credentials": {},
                "credentials_token_request": {},
                "use_local_token": None,
            },
        )
        self.assertEqual(
            _parse_parameters(wait_until="networkidle0"),
            {
                "arg_viewport": {},
                "screenshot_options": {"fullPage": False},
                "selector": None,
                "wait_for": None,
                "wait_for_xpath": None,
                "wait_until": ["networkidle0"],
                "credentials": {},
                "credentials_token_request": {},
                "use_local_token": None,
            },
        )
        self.assertEqual(
            _parse_parameters(full_page=True),
            {
                "arg_viewport": {},
                "screenshot_options": {"fullPage": True},
                "selector": None,
                "wait_for": None,
                "wait_for_xpath": None,
                "wait_until": ["load"],
                "credentials": {},
                "credentials_token_request": {},
                "use_local_token": None,
            },
        )
        self.assertEqual(
            _parse_parameters(selector="div"),
            {
                "arg_viewport": {},
                "screenshot_options": {"fullPage": False},
                "selector": "div",
                "wait_for": None,
                "wait_for_xpath": None,
                "wait_until": ["load"],
                "credentials": {},
                "credentials_token_request": {},
                "use_local_token": None,
            },
        )
        self.assertEqual(
            _parse_parameters(wait_for="div"),
            {
                "arg_viewport": {},
                "screenshot_options": {"fullPage": False},
                "selector": None,
                "wait_for": "div",
                'wait_for_xpath': None,
                "wait_until": ["load"],
                "credentials": {},
                "credentials_token_request": {},
                "use_local_token": None,
            },
        )
        self.assertEqual(
            _parse_parameters(wait_for_xpath="div"),
            {
                "arg_viewport": {},
                "screenshot_options": {"fullPage": False},
                "selector": None,
                "wait_for": None,
                'wait_for_xpath': "div",
                "wait_until": ["load"],
                "credentials": {},
                "credentials_token_request": {},
                "use_local_token": None,
            },
        )
        self.assertEqual(
            _parse_parameters(path="/"),
            {
                "arg_viewport": {},
                "screenshot_options": {"fullPage": False, "path": "/"},
                "selector": None,
                "wait_for": None,
                "wait_for_xpath": None,
                "wait_until": ["load"],
                "credentials": {},
                "credentials_token_request": {},
                "use_local_token": None,
            },
        )
        self.assertEqual(
            _parse_parameters(
                credentials={"username": "makina", "password": "makina"}),
            {
                "arg_viewport": {},
                "screenshot_options": {"fullPage": False},
                "selector": None,
                "wait_for": None,
                "wait_for_xpath": None,
                "wait_until": ["load"],
                "credentials": {
                    "login": True,
                    "credentials_data": {"username": "makina", "password": "makina"},
                },
                "credentials_token_request": {},
                "use_local_token": None,
            },
        )
        self.assertEqual(
            _parse_parameters(
                credentials={"token_in_header": True, "token": "xxx"}),
            {
                "arg_viewport": {},
                "screenshot_options": {"fullPage": False},
                "selector": None,
                "wait_for": None,
                "wait_for_xpath": None,
                "wait_until": ["load"],
                "credentials": {
                    "token_in_header": True,
                    "credentials_data": {"token": "xxx"},
                },
                "credentials_token_request": {},
                "use_local_token": None,
            },
        )
        self.assertEqual(
            _parse_parameters(url_token="http://fake",
                              username_token="me", password_token="1234"),
            {
                "arg_viewport": {},
                "screenshot_options": {"fullPage": False},
                "selector": None,
                "wait_for": None,
                "wait_for_xpath": None,
                "wait_until": ["load"],
                "credentials": {},
                "credentials_token_request": {
                    "url": "http://fake",
                    "username": "me",
                    "password": "1234",
                    "local_storage": False,
                },
                "use_local_token": None,
            },
        )

    @patch("screamshot.generate_bytes_img_functions.get_token")
    @patch("screamshot.generate_bytes_img_functions.get_local_storage_token")
    def test_page_manager(self, mock_get_token, mock_get_local_storage_token):
        """
        Tests _page_manager
        """
        browser = FakeBrowser()
        url = "http://fake"
        mock_get_token.return_value = {"token": "xxx"}
        mock_get_local_storage_token.return_value = {"token": "xxx"}

        params_page1 = {
            "arg_viewport": {},
            "screenshot_options": {"fullPage": False},
            "selector": None,
            "wait_for": None,
            "wait_for_xpath": None,
            "wait_until": ["load"],
            "credentials": {},
            "credentials_token_request": {},
            "use_local_token": None,
        }
        page1 = to_sync(_page_manager(browser, url, params_page1))
        self.assertEqual(page1.arg_viewport, None)
        self.assertEqual(page1.credentials, None)
        self.assertEqual(page1.wait_until, ["load"])
        self.assertTrue(page1.goto_called)
        self.assertEqual(page1.url, url)
        self.assertFalse(page1.waitForSelector_called)
        self.assertEqual(page1.wait_for, None)
        self.assertFalse(page1.querySelector_called)
        self.assertEqual(page1.selector, None)

        params_page2 = {
            "arg_viewport": {"width": 800, "height": 800},
            "screenshot_options": {"fullPage": False},
            "selector": None,
            "wait_for": None,
            "wait_for_xpath": None,
            "wait_until": ["load"],
            "credentials": {},
            "credentials_token_request": {},
            "use_local_token": None,
        }
        page2 = to_sync(_page_manager(browser, url, params_page2))
        self.assertEqual(page2.arg_viewport, {"width": 800, "height": 800})
        self.assertEqual(page2.credentials, None)
        self.assertEqual(page2.wait_until, ["load"])
        self.assertTrue(page2.goto_called)
        self.assertEqual(page2.url, url)
        self.assertFalse(page2.waitForSelector_called)
        self.assertEqual(page2.wait_for, None)
        self.assertFalse(page2.querySelector_called)
        self.assertEqual(page2.selector, None)

        params_page3 = {
            "arg_viewport": {},
            "screenshot_options": {"fullPage": False},
            "selector": None,
            "wait_for": None,
            "wait_for_xpath": None,
            "wait_until": ["load", "networkidle0"],
            "credentials": {},
            "credentials_token_request": {},
            "use_local_token": None,
        }
        page3 = to_sync(_page_manager(browser, url, params_page3))
        self.assertEqual(page3.arg_viewport, None)
        self.assertEqual(page3.credentials, None)
        self.assertEqual(page3.wait_until, ["load", "networkidle0"])
        self.assertTrue(page3.goto_called)
        self.assertEqual(page3.url, url)
        self.assertFalse(page3.waitForSelector_called)
        self.assertEqual(page3.wait_for, None)
        self.assertFalse(page3.querySelector_called)
        self.assertEqual(page3.selector, None)

        params_page4 = {
            "arg_viewport": {},
            "screenshot_options": {"fullPage": False},
            "selector": None,
            "wait_for": "div",
            "wait_until": ["load"],
            "credentials": {},
            "credentials_token_request": {},
            "use_local_token": None,
        }
        page4 = to_sync(_page_manager(browser, url, params_page4))
        self.assertEqual(page4.arg_viewport, None)
        self.assertEqual(page4.credentials, None)
        self.assertEqual(page4.wait_until, ["load"])
        self.assertTrue(page4.goto_called)
        self.assertEqual(page4.url, url)
        self.assertTrue(page4.waitForSelector_called)
        self.assertEqual(page4.wait_for, "div")
        self.assertFalse(page4.querySelector_called)
        self.assertEqual(page4.selector, None)

        params_page5 = {
            "arg_viewport": {},
            "screenshot_options": {"fullPage": False},
            "selector": None,
            "wait_for": "div",
            "wait_until": ["load"],
            "credentials": {
                "login": True,
                "credentials_data": {"username": "makina", "password": "makina"},
            },
            "credentials_token_request": {},
            "use_local_token": None,
        }
        page5 = to_sync(_page_manager(browser, url, params_page5))
        self.assertEqual(page5.arg_viewport, None)
        self.assertEqual(
            page5.credentials, {"username": "makina", "password": "makina"}
        )
        self.assertEqual(page5.wait_until, ["load"])
        self.assertTrue(page5.goto_called)
        self.assertEqual(page5.url, url)
        self.assertTrue(page5.waitForSelector_called)
        self.assertEqual(page5.wait_for, "div")
        self.assertFalse(page5.querySelector_called)
        self.assertEqual(page5.selector, None)

        params_page6 = {
            "arg_viewport": {},
            "screenshot_options": {"fullPage": False},
            "selector": None,
            "wait_for": "div",
            "wait_until": ["load"],
            "credentials": {
                "token_in_header": True,
                "credentials_data": {"token": "xxx"},
            },
            "credentials_token_request": {},
            "use_local_token": None,
        }
        page6 = to_sync(_page_manager(browser, url, params_page6))
        self.assertEqual(page6.arg_viewport, None)
        self.assertEqual(page6.credentials, {"token": "xxx"})
        self.assertEqual(page6.wait_until, ["load"])
        self.assertTrue(page6.goto_called)
        self.assertEqual(page6.url, url)
        self.assertTrue(page6.waitForSelector_called)
        self.assertEqual(page6.wait_for, "div")
        self.assertFalse(page6.querySelector_called)
        self.assertEqual(page6.selector, None)

        params_page7 = {
            "arg_viewport": {},
            "screenshot_options": {"fullPage": False},
            "selector": None,
            "wait_for_xpath": "div",
            "wait_until": ["load"],
            "credentials": {},
            "credentials_token_request": {},
            "use_local_token": None,
        }
        page7 = to_sync(_page_manager(browser, url, params_page7))
        self.assertEqual(page7.arg_viewport, None)
        self.assertEqual(page7.credentials, None)
        self.assertEqual(page7.wait_until, ["load"])
        self.assertTrue(page7.goto_called)
        self.assertEqual(page7.url, url)
        self.assertFalse(page7.waitForSelector_called)
        self.assertEqual(page7.wait_for, None)
        self.assertTrue(page7.waitForxPath_called)
        self.assertEqual(page7.wait_for_xpath, "div")
        self.assertFalse(page7.querySelector_called)
        self.assertEqual(page7.selector, None)

        params_page8 = {
            "arg_viewport": {},
            "screenshot_options": {"fullPage": False},
            "selector": None,
            "wait_for_xpath": "div",
            "wait_until": ["load"],
            "credentials": {},
            "credentials_token_request": {"url": "http://fake", "username": "me", "password": "1234", "local_storage": False},
            "use_local_token": None,
        }
        page8 = to_sync(_page_manager(browser, url, params_page8))
        self.assertEqual(page8.arg_viewport, None)
        self.assertEqual(page8.credentials, {"token": "xxx"})
        self.assertEqual(page8.wait_until, ["load"])
        self.assertTrue(page8.goto_called)
        self.assertEqual(page8.url, url)
        self.assertFalse(page8.waitForSelector_called)
        self.assertEqual(page8.wait_for, None)
        self.assertTrue(page8.waitForxPath_called)
        self.assertEqual(page8.wait_for_xpath, "div")
        self.assertFalse(page8.querySelector_called)
        self.assertEqual(page8.selector, None)

        params_page9 = {
            "arg_viewport": {},
            "screenshot_options": {"fullPage": False},
            "selector": None,
            "wait_for_xpath": "div",
            "wait_until": ["load"],
            "credentials": {},
            "credentials_token_request": {"url": "http://fake", "username": "me", "password": "1234", "local_storage": True},
            "use_local_token": True,
        }
        page9 = to_sync(_page_manager(browser, url, params_page9))
        self.assertEqual(page9.arg_viewport, None)
        self.assertEqual(page9.credentials, {"token": "xxx"})
        self.assertEqual(page9.wait_until, ["load"])
        self.assertTrue(page9.goto_called)
        self.assertEqual(page9.url, url)
        self.assertFalse(page9.waitForSelector_called)
        self.assertEqual(page9.wait_for, None)
        self.assertTrue(page9.waitForxPath_called)
        self.assertEqual(page9.wait_for_xpath, "div")
        self.assertFalse(page9.querySelector_called)
        self.assertEqual(page9.selector, None)

        params_page10 = {
            "arg_viewport": {},
            "screenshot_options": {"fullPage": False},
            "selector": None,
            "wait_for_xpath": "div",
            "wait_until": ["load"],
            "credentials": {},
            "credentials_token_request": {},
            "use_local_token": True,
        }
        page10 = to_sync(_page_manager(browser, url, {
            "arg_viewport": {},
            "screenshot_options": {"fullPage": False},
            "selector": None,
            "wait_for_xpath": "div",
            "wait_until": ["load"],
            "credentials": {},
            "credentials_token_request": {
                "url": "http://fake", "username": "me", "password": "1234", "local_storage": True
            },
            "use_local_token": True,
        }))
        page10 = to_sync(_page_manager(browser, url, params_page10))
        self.assertEqual(page10.arg_viewport, None)
        self.assertEqual(page10.credentials, {"token": "xxx"})
        self.assertEqual(page10.wait_until, ["load"])
        self.assertTrue(page10.goto_called)
        self.assertEqual(page10.url, url)
        self.assertFalse(page10.waitForSelector_called)
        self.assertEqual(page10.wait_for, None)
        self.assertTrue(page10.waitForxPath_called)
        self.assertEqual(page10.wait_for_xpath, "div")
        self.assertFalse(page10.querySelector_called)
        self.assertEqual(page10.selector, None)

    def test_selector_manager(self):
        """
        Tests _selector_manager
        """
        url = "http://fake"

        params_page1 = {
            "arg_viewport": {},
            "screenshot_options": {"fullPage": False},
            "selector": None,
            "wait_for": None,
            "wait_for_xpath": None,
            "wait_until": ["load"],
        }
        page1 = FakePage(
            arg_viewport=None,
            wait_until=["load"],
            goto_called=True,
            url=url,
            waitForSelector_called=False,
            wait_for=None,
        )
        new_page1 = to_sync(_selector_manager(page1, params_page1))
        self.assertEqual(new_page1.arg_viewport, None)
        self.assertEqual(new_page1.wait_until, ["load"])
        self.assertTrue(new_page1.goto_called)
        self.assertEqual(new_page1.url, url)
        self.assertFalse(new_page1.waitForSelector_called)
        self.assertEqual(new_page1.wait_for, None)
        self.assertFalse(new_page1.querySelector_called)
        self.assertEqual(new_page1.selector, None)

        params_page2 = {
            "arg_viewport": {},
            "screenshot_options": {"fullPage": False},
            "selector": "div",
            "wait_for": None,
            "wait_for_xpath": None,
            "wait_until": ["load"],
        }
        page2 = FakePage(
            arg_viewport=None,
            wait_until=["load"],
            goto_called=True,
            url=url,
            waitForSelector_called=False,
            wait_for=None,
        )
        new_page2 = to_sync(_selector_manager(page2, params_page2))
        self.assertEqual(new_page2.arg_viewport, None)
        self.assertEqual(new_page2.wait_until, ["load"])
        self.assertTrue(new_page2.goto_called)
        self.assertEqual(new_page2.url, url)
        self.assertFalse(new_page2.waitForSelector_called)
        self.assertEqual(new_page2.wait_for, None)
        self.assertTrue(new_page2.querySelector_called)
        self.assertEqual(new_page2.selector, "div")

    @patch("screamshot.generate_bytes_img_functions.get_browser")
    def test_generate_bytes_img(self, mock_get_browser):
        """
        Tests generate_bytes_img
        """
        mock_get_browser.side_effect = get_browser

        url = "http://fake"

        screenshot1 = to_sync(generate_bytes_img(url))
        self.assertEqual(screenshot1, "screenshot !")

    @patch("screamshot.generate_bytes_img_functions.get_browser")
    def test_generate_bytes_img_prom(self, mock_get_browser):
        """
        Tests_generate_bytes_img_prom
        """
        mock_get_browser.side_effect = get_browser

        url = "http://fake"

        loop = get_event_loop()
        future = Future()
        ensure_future(generate_bytes_img_prom(url, future))
        loop.run_until_complete(future)
        screenshot1 = future.result()
        self.assertEqual(screenshot1, "screenshot !")
