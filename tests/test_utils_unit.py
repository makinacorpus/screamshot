"""
Unit tests of `utils.py` functions
"""
from os import remove
from unittest import TestCase
from unittest import mock

from urllib3.exceptions import MaxRetryError

from requests.exceptions import ConnectionError as RequestsConnectionError

from screamshot.utils import (
    to_sync,
    _check_wait_until_arg,
    url_match,
    set_endpoint,
    FILENAME_ENDPOINT,
    get_endpoint,
    open_browser,
    get_browser,
    wait_server_start,
    wait_server_close,
    get_token,
    get_token_local_storage,
)
from screamshot.errors import BadAuth

from _io import TextIOWrapper


class FakeBrowser:
    def __init__(self, headless, autoClose, args):
        self.headless = headless
        self.autoClose = autoClose
        self.args = args
        self.wsEndpoint = "wsEndpoint"


async def mocked_launch(options=None, **kwargs):
    parameters = dict()
    if options:
        parameters.update(options)
    parameters.update(kwargs)

    headless = parameters.get("headless")
    if not headless:
        headless = False

    autoClose = parameters.get("autoClose", True)

    args = parameters.get("args")

    browser = FakeBrowser(headless, autoClose, args)
    return browser


def mocked_set_endpoint(ws_endpoint):
    raise ValueError(ws_endpoint)


async def mocked_connect(browserWSEndpoint=None):
    raise ValueError("connect !")


async def mocked_open_browser(is_headless, launch_args=None, write_websocket=True):
    raise ValueError("open_browser !")


class UnistTestsUtilsFunctions(TestCase):
    """
    Test class
    """

    def test_check_wait_until_arg(self):
        """
        Tests _check_wait_until_arg
        """
        self.assertTrue(_check_wait_until_arg("load"))
        self.assertTrue(_check_wait_until_arg(["load"]))

        self.assertTrue(_check_wait_until_arg("domcontentloaded"))
        self.assertTrue(_check_wait_until_arg(["domcontentloaded"]))

        self.assertTrue(_check_wait_until_arg("networkidle0"))
        self.assertTrue(_check_wait_until_arg(["networkidle0"]))

        self.assertTrue(_check_wait_until_arg("networkidle2"))
        self.assertTrue(_check_wait_until_arg(["networkidle2"]))

        self.assertFalse(_check_wait_until_arg("no"))
        self.assertFalse(_check_wait_until_arg(["no"]))

    def test_url_match(self):
        """
        Tests url_match
        """
        self.assertTrue(url_match("https://www.google.fr", "https://www.google.fr"))
        self.assertTrue(url_match("https://www.google.fr/", "https://www.google.fr"))
        self.assertTrue(url_match("https://www.google.fr", "https://www.google.fr/"))

        self.assertFalse(url_match("http://www.google.fr", "https://www.google.fr"))
        self.assertFalse(url_match("http://www.google.fr/", "https://www.google.fr"))
        self.assertFalse(url_match("http://www.google.fr", "https://www.google.fr/"))

    def test_set_endpoint(self):
        """
        Tests set_endpoint
        """
        with self.assertRaises(FileNotFoundError):
            open(FILENAME_ENDPOINT, "r")

        set_endpoint("toto")
        endpoint_f = open(FILENAME_ENDPOINT, "r")
        self.assertTrue(isinstance(endpoint_f, TextIOWrapper))
        endpoint_fc = endpoint_f.readlines()
        self.assertEqual(len(endpoint_fc), 1)
        endpoint = endpoint_fc[0][:-1]
        self.assertEqual("toto", endpoint)

        endpoint_f.close()
        remove(FILENAME_ENDPOINT)

    def test_get_end_point(self):
        """
        Tests get_end_point
        """
        self.assertEqual(get_endpoint(), None)

        with self.assertLogs() as logs:
            get_endpoint()
        self.assertEqual(
            logs.output, ["WARNING:root:{0} not found".format(FILENAME_ENDPOINT)]
        )

        endpoint_f = open(FILENAME_ENDPOINT, "w")
        endpoint_f.write("toto\n")
        endpoint_f.close()
        self.assertEqual(get_endpoint(), "toto")

        remove(FILENAME_ENDPOINT)

    @mock.patch("screamshot.utils.set_endpoint")
    @mock.patch("screamshot.utils.launch")
    def test_open_browser(self, mock_launch, mock_set_endpoint):
        mock_launch.side_effect = mocked_launch
        mock_set_endpoint.side_effect = mocked_set_endpoint

        browser1 = to_sync(open_browser(True, write_websocket=False))
        self.assertTrue(browser1.headless)
        self.assertFalse(browser1.autoClose)
        self.assertEqual(browser1.args, None)
        self.assertEqual(browser1.wsEndpoint, "wsEndpoint")

        browser2 = to_sync(open_browser(False, write_websocket=False))
        self.assertFalse(browser2.headless)
        self.assertFalse(browser2.autoClose)
        self.assertEqual(browser2.args, None)
        self.assertEqual(browser2.wsEndpoint, "wsEndpoint")

        browser3 = to_sync(
            open_browser(True, launch_args=["--no-sandbox"], write_websocket=False)
        )
        self.assertTrue(browser3.headless)
        self.assertFalse(browser3.autoClose)
        self.assertEqual(browser3.args, ["--no-sandbox"])
        self.assertEqual(browser3.wsEndpoint, "wsEndpoint")

        with self.assertRaisesRegex(ValueError, "wsEndpoint"):
            browser4 = to_sync(open_browser(True, launch_args=["--no-sandbox"]))
            self.assertTrue(browser4.headless)
            self.assertFalse(browser4.autoClose)
            self.assertEqual(browser4.args, ["--no-sandbox"])
            self.assertEqual(browser4.wsEndpoint, "wsEndpoint")

    @mock.patch("screamshot.utils.get_endpoint")
    @mock.patch("screamshot.utils.connect")
    @mock.patch("screamshot.utils.open_browser")
    def test_get_browser(self, mock_open_browser, mock_connect, mock_get_endpoint):
        mock_connect.side_effect = mocked_connect
        mock_open_browser.side_effect = mocked_open_browser

        mock_get_endpoint.return_value = "endpoint"
        with self.assertRaisesRegex(ValueError, "connect !"):
            to_sync(get_browser())

        mock_get_endpoint.return_value = None
        with self.assertRaisesRegex(ValueError, "open_browser !"):
            to_sync(get_browser())

    @mock.patch("screamshot.utils.get")
    def test_wait_server_start(self, mock_get):
        """
        Tests wait_server_start
        """
        mock_get.side_effect = MaxRetryError(None, "http://false")
        with self.assertRaises(MaxRetryError):
            with self.assertLogs() as logs:
                wait_server_start("http://false", "Wait for: %ds", "")
        self.assertEqual(
            logs.output,
            [
                "INFO:root:Wait for: 0s",
                "INFO:root:Wait for: 1s",
                "INFO:root:Wait for: 2s",
                "INFO:root:Wait for: 3s",
                "INFO:root:Wait for: 4s",
                "INFO:root:Wait for: 5s",
                "INFO:root:Wait for: 6s",
                "INFO:root:Wait for: 7s",
                "INFO:root:Wait for: 8s",
                "INFO:root:Wait for: 9s",
            ],
        )

        mock_response = mock.Mock()
        mock_response.status_code.return_value = 200
        mock_get.side_effect = [MaxRetryError(None, "http://false"), mock_response]
        with self.assertLogs() as logs:
            wait_server_start("http://false", "Wait for: %ds", "Awaited: %ds")
        self.assertEqual(
            logs.output, ["INFO:root:Wait for: 0s", "INFO:root:Awaited: 1s"]
        )

        mock_get.side_effect = mock_response
        with self.assertLogs() as logs:
            wait_server_start("http://false", "Wait for: %ds", "Awaited: %ds")
        self.assertEqual(logs.output, ["INFO:root:Awaited: 0s"])

    @mock.patch("screamshot.utils.get")
    def test_wait_server_close(self, mock_get):
        """
        Tests wait_server_close
        """
        mock_response = mock.Mock()
        mock_response.status_code.return_value = 200
        mock_get.side_effect = mock_response
        with self.assertRaises(MaxRetryError):
            with self.assertLogs() as logs:
                wait_server_close("http://false", "Wait for: %ds", "")
        self.assertEqual(
            logs.output,
            [
                "INFO:root:Wait for: 0s",
                "INFO:root:Wait for: 1s",
                "INFO:root:Wait for: 2s",
                "INFO:root:Wait for: 3s",
                "INFO:root:Wait for: 4s",
                "INFO:root:Wait for: 5s",
                "INFO:root:Wait for: 6s",
                "INFO:root:Wait for: 7s",
                "INFO:root:Wait for: 8s",
                "INFO:root:Wait for: 9s",
            ],
        )

        mock_response = mock.Mock()
        mock_response.status_code.return_value = 200
        mock_get.side_effect = [mock_response, RequestsConnectionError()]
        with self.assertLogs() as logs:
            wait_server_close("http://false", "Wait for: %ds", "Awaited: %ds")
        self.assertEqual(
            logs.output, ["INFO:root:Wait for: 0s", "INFO:root:Awaited: 1s"]
        )

        mock_get.side_effect = RequestsConnectionError()
        with self.assertLogs() as logs:
            wait_server_close("http://false", "Wait for: %ds", "Awaited: %ds")
        self.assertEqual(logs.output, ["INFO:root:Awaited: 0s"])

    @mock.patch("screamshot.utils.post")
    def test_get_token_200(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.content = '{"token": "hey you"}'
        self.assertEqual(get_token("http://false", {}), '{"token": "hey you"}')

    @mock.patch("screamshot.utils.post")
    def test_get_token_400(self, mock_post):
        mock_post.return_value.status_code = 400
        mock_post.return_value.content = '{"token": "hey you"}'
        with self.assertRaises(BadAuth):
            get_token("http://false", {})

    @mock.patch("screamshot.utils.post")
    def test_get_token_local_storage(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.content = '{"token": "hey you"}'
        browser = to_sync(open_browser(True, write_websocket=False, launch_args=["--no-sandbox"]))
        page = to_sync(browser.newPage())
        to_sync(page.goto('http://duckduckgo.com'))
        to_sync(get_token_local_storage("http://false", {}, page))
        token = to_sync(page.evaluate("() => window.localStorage.getItem('token')"))
        self.assertEqual(token, '{"token": "hey you"}')
        browser.close()
