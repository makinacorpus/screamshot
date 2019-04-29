"""
Unit tests of `generate_bytes_img_function.py`
"""
from unittest import TestCase, main
from unittest.mock import patch
from asyncio import get_event_loop, Future, ensure_future

from screamshot.generate_bytes_img_functions import (_parse_parameters, _page_manager,
                                                     _selector_manager, generate_bytes_img,
                                                     generate_bytes_img_prom)
from screamshot.utils import to_sync


class FakePage:
    def __init__(self, arg_viewport=None, wait_until=None, goto_called=False, url=None,
                 waitForSelector_called=False, wait_for=None, querySelector_called=False,
                 selector=None):
        self.arg_viewport = arg_viewport
        self.wait_until = wait_until
        self.goto_called = goto_called
        self.url = url
        self.waitForSelector_called = waitForSelector_called
        self.wait_for = wait_for
        self.querySelector_called = querySelector_called
        self.selector = selector

    def setViewport(self, arg_viewport):
        self.arg_viewport = arg_viewport

    async def goto(self, url, waitUntil=None):
        self.goto_called = True
        self.url = url
        self.wait_until = waitUntil

    async def waitForSelector(self, wait_for):
        self.waitForSelector_called = True
        self.wait_for = wait_for

    async def querySelector(self, selector):
        self.querySelector_called = True
        self.selector = selector
        return self

    async def screenshot(self, **kwargs):
        return 'screenshot !'

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
        self.assertEqual(_parse_parameters(),
                         {'arg_viewport': {},
                          'screenshot_options': {'fullPage': False}, 'selector': None,
                          'wait_for': None, 'wait_until': ['load']})
        self.assertEqual(_parse_parameters(width=800),
                         {'arg_viewport': {'width': 800},
                          'screenshot_options': {'fullPage': False},
                          'selector': None, 'wait_for': None, 'wait_until': ['load']})
        self.assertEqual(_parse_parameters(height=800),
                         {'arg_viewport': {'height': 800},
                          'screenshot_options': {'fullPage': False},
                          'selector': None, 'wait_for': None, 'wait_until': ['load']})
        self.assertEqual(_parse_parameters(wait_until=['networkidle0']),
                         {'arg_viewport': {},
                          'screenshot_options': {'fullPage': False}, 'selector': None,
                          'wait_for': None, 'wait_until': ['networkidle0']})
        self.assertEqual(_parse_parameters(wait_until='networkidle0'),
                         {'arg_viewport': {},
                          'screenshot_options': {'fullPage': False}, 'selector': None,
                          'wait_for': None, 'wait_until': ['networkidle0']})
        self.assertEqual(_parse_parameters(full_page=True),
                         {'arg_viewport': {},
                          'screenshot_options': {'fullPage': True}, 'selector': None,
                          'wait_for': None, 'wait_until': ['load']})
        self.assertEqual(_parse_parameters(selector='div'),
                         {'arg_viewport': {},
                          'screenshot_options': {'fullPage': False}, 'selector': 'div',
                          'wait_for': None, 'wait_until': ['load']})
        self.assertEqual(_parse_parameters(wait_for='div'),
                         {'arg_viewport': {},
                          'screenshot_options': {'fullPage': False}, 'selector': None,
                          'wait_for': 'div', 'wait_until': ['load']})
        self.assertEqual(_parse_parameters(path='/'),
                         {'arg_viewport': {},
                          'screenshot_options': {'fullPage': False, 'path': '/'}, 'selector': None,
                          'wait_for': None, 'wait_until': ['load']})

    def test_page_manager(self):
        """
        Tests _page_manager
        """
        browser = FakeBrowser()
        url = 'http://fake'

        params_page1 = {'arg_viewport': {}, 'screenshot_options': {'fullPage': False},
                        'selector': None, 'wait_for': None, 'wait_until': ['load']}
        page1 = to_sync(_page_manager(browser, url, params_page1))
        self.assertEqual(page1.arg_viewport, None)
        self.assertEqual(page1.wait_until, ['load'])
        self.assertTrue(page1.goto_called)
        self.assertEqual(page1.url, url)
        self.assertFalse(page1.waitForSelector_called)
        self.assertEqual(page1.wait_for, None)
        self.assertFalse(page1.querySelector_called)
        self.assertEqual(page1.selector, None)

        params_page2 = {'arg_viewport': {'width': 800, 'height': 800},
                        'screenshot_options': {'fullPage': False},
                        'selector': None, 'wait_for': None, 'wait_until': ['load']}
        page2 = to_sync(_page_manager(browser, url, params_page2))
        self.assertEqual(page2.arg_viewport, {'width': 800, 'height': 800})
        self.assertEqual(page2.wait_until, ['load'])
        self.assertTrue(page2.goto_called)
        self.assertEqual(page2.url, url)
        self.assertFalse(page2.waitForSelector_called)
        self.assertEqual(page2.wait_for, None)
        self.assertFalse(page2.querySelector_called)
        self.assertEqual(page2.selector, None)

        params_page3 = {'arg_viewport': {}, 'screenshot_options': {'fullPage': False},
                        'selector': None, 'wait_for': None, 'wait_until': ['load', 'networkidle0']}
        page3 = to_sync(_page_manager(browser, url, params_page3))
        self.assertEqual(page3.arg_viewport, None)
        self.assertEqual(page3.wait_until, ['load', 'networkidle0'])
        self.assertTrue(page3.goto_called)
        self.assertEqual(page3.url, url)
        self.assertFalse(page3.waitForSelector_called)
        self.assertEqual(page3.wait_for, None)
        self.assertFalse(page3.querySelector_called)
        self.assertEqual(page3.selector, None)

        params_page4 = {'arg_viewport': {}, 'screenshot_options': {'fullPage': False},
                        'selector': None, 'wait_for': 'div', 'wait_until': ['load']}
        page4 = to_sync(_page_manager(browser, url, params_page4))
        self.assertEqual(page4.arg_viewport, None)
        self.assertEqual(page4.wait_until, ['load'])
        self.assertTrue(page4.goto_called)
        self.assertEqual(page4.url, url)
        self.assertTrue(page4.waitForSelector_called)
        self.assertEqual(page4.wait_for, 'div')
        self.assertFalse(page4.querySelector_called)
        self.assertEqual(page4.selector, None)


    def test_selector_manager(self):
        """
        Tests _selector_manager
        """
        url = 'http://fake'

        params_page1 = {'arg_viewport': {}, 'screenshot_options': {'fullPage': False},
                        'selector': None, 'wait_for': None, 'wait_until': ['load']}
        page1 = FakePage(arg_viewport=None, wait_until=['load'], goto_called=True, url=url,
                         waitForSelector_called=False, wait_for=None)
        new_page1 = to_sync(_selector_manager(page1, params_page1))
        self.assertEqual(new_page1.arg_viewport, None)
        self.assertEqual(new_page1.wait_until, ['load'])
        self.assertTrue(new_page1.goto_called)
        self.assertEqual(new_page1.url, url)
        self.assertFalse(new_page1.waitForSelector_called)
        self.assertEqual(new_page1.wait_for, None)
        self.assertFalse(new_page1.querySelector_called)
        self.assertEqual(new_page1.selector, None)

        params_page2 = {'arg_viewport': {}, 'screenshot_options': {'fullPage': False},
                        'selector': 'div', 'wait_for': None, 'wait_until': ['load']}
        page2 = FakePage(arg_viewport=None, wait_until=['load'], goto_called=True, url=url,
                         waitForSelector_called=False, wait_for=None)
        new_page2 = to_sync(_selector_manager(page2, params_page2))
        self.assertEqual(new_page2.arg_viewport, None)
        self.assertEqual(new_page2.wait_until, ['load'])
        self.assertTrue(new_page2.goto_called)
        self.assertEqual(new_page2.url, url)
        self.assertFalse(new_page2.waitForSelector_called)
        self.assertEqual(new_page2.wait_for, None)
        self.assertTrue(new_page2.querySelector_called)
        self.assertEqual(new_page2.selector, 'div')

    @patch('screamshot.generate_bytes_img_functions.get_browser')
    def test_generate_bytes_img(self, mock_get_browser):
        """
        Tests generate_bytes_img
        """
        mock_get_browser.side_effect = get_browser

        url = 'http://fake'

        screenshot1 = to_sync(generate_bytes_img(url))
        self.assertEqual(screenshot1, 'screenshot !')

    @patch('screamshot.generate_bytes_img_functions.get_browser')
    def test_generate_bytes_img_prom(self, mock_get_browser):
        """
        Tests_generate_bytes_img_prom
        """
        mock_get_browser.side_effect = get_browser

        url = 'http://fake'

        loop = get_event_loop()
        future = Future()
        ensure_future(generate_bytes_img_prom(url, future))
        loop.run_until_complete(future)
        screenshot1 = future.result()
        self.assertEqual(screenshot1, 'screenshot !')




if __name__ == '__main__':
    main()
