"""
Collection of functions.
"""
import logging
import asyncio
from os import remove
from os.path import join
from time import sleep
from typing import Any, Optional
from tempfile import gettempdir

from urllib3.exceptions import MaxRetryError

from requests import get, post
from requests.exceptions import ConnectionError as RequestsConnectionError

from pyppeteer import launch, connect
from pyppeteer.browser import Browser
from screamshot.errors import BadAuth


FILENAME_ENDPOINT = join(gettempdir(), "screamshot_browser_endpoint")


logger = logging.getLogger()

logger.setLevel(logging.WARNING)

formatter = logging.Formatter("%(asctime)s :: %(levelname)s :: %(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


def _check_wait_until_arg(wait_until_arg: list) -> bool:
    values = ["load", "domcontentloaded", "networkidle0", "networkidle2"]
    return wait_until_arg in values or all([arg in values for arg in wait_until_arg])


def to_sync(fun: Any) -> Any:
    """
    This synchronous function execute and returns the result of an asynchronous function

    :param fun: mandatory, the asynchronous function
    :type fun: function

    .. warning :: This function uses `asyncio` package
    """
    return asyncio.get_event_loop().run_until_complete(fun)


def url_match(url1: str, url2: str) -> bool:
    """
    This function takes two urls and check if they are the same modulo '/' at the end
    :param url1: mandatory, the first url
    :type url1: str

    :param url2: mandatory, the second url
    :type url2: str

    :rtype: Boolean
    """
    return url1 == url2 or url1[:-1] == url2 or url1 == url2[:-1]


def set_endpoint(ws_endpoint: str):
    """
    This function store the web socket endpoint of the launched browser

    :param ws_endpoint: mandatory, the web socket endpoint
    :type ws_endpoint: str

    .. note :: ws_endpoint is saved in FILENAME_ENDPOINT

    .. warning :: It must have the following form: http://.../..., for get_endpoint to work
    """
    with open(FILENAME_ENDPOINT, "w") as ws_file:
        ws_file.write(ws_endpoint + "\n")


def get_endpoint() -> Optional[str]:
    """
    This function returns the web socket endpoint of the running browser

    :retype: str

    .. note :: ws_endpoint is retrieved from FILENAME_ENDPOINT
    """
    try:
        with open(FILENAME_ENDPOINT, "r") as ws_file:
            line = ws_file.readline()
            line = line.split()[0]
            return line
    except FileNotFoundError:
        logger.warning(str(FILENAME_ENDPOINT + " not found"))
        return None


async def open_browser(
        is_headless: bool, launch_args: list = None, write_websocket: bool = True
) -> Browser:
    """
    Launch a browser and writes its websocket endpoint in FILENAME_ENDPOINT if needed

    :param is_headless: mandatory, should the browser be launched in headless mode ?
    :type is_headless: bool

    :param write_websocket: optional, should we store the websocket endpoint in FILENAME_ENDPOINT ?
    :type write_websocket: bool

    :param launch_args: optional, other optional parameters use
    :type launch_args: list of str

    :return: the opened browser
    :retype: pyppeteer Browser
    """
    browser = await launch(headless=is_headless, autoClose=False, args=launch_args)
    if write_websocket:
        set_endpoint(browser.wsEndpoint)
    return browser


async def close_browser():
    """
    Closes the browser related to ws_endpoint and remove FILENAME_ENDPOINT
    """
    ws_endpoint = get_endpoint()
    if ws_endpoint:
        browser = await connect(browserWSEndpoint=ws_endpoint)
        await browser.close()
        remove(FILENAME_ENDPOINT)


async def get_browser(
        is_headless: bool = True, launch_args: list = None, write_websocket: bool = True
) -> Browser:
    """
    Returns a already created browser if one exists or a new one if not

    :param is_headless: optionnal, should the browser be launched in headless mode ?
    :type is_headless: bool

    :param write_websocket: optional, should we store the websocket endpoint in FILENAME_ENDPOINT ?
    :type write_websocket: bool

    :retype: pyppeteer.browser.Browser
    """
    endpoint = get_endpoint()
    if endpoint:
        return await connect(browserWSEndpoint=endpoint)
    return await open_browser(
        is_headless, launch_args=launch_args, write_websocket=write_websocket
    )


def get_token(url, data, local_storage=False, page=None):
    """
    Returns the token fetched to an url

    :param url: The url to visit
    :type url: str

    :param data: credentials data to use
    :type data: dict

    :param local_storage: should we store the request content in the local storage
    :type local_storage: Boolean

    :param page: page used for the local storage
    :type page: pyppeteer.page.Page

    :retype: dict

    ..warning:: Raises BadAuth error if the response hasn't the status code 200
    """
    request = post(url, data=data)
    if not request.status_code == 200:
        raise BadAuth("Server response {}".format(request.status_code))
    if local_storage and page:
        to_sync(page.evaluate(
            "() => window.localStorage.setItem('token', '{}')".format(request.content)))
    return request.content


def wait_server_start(url: str, waiting_message: str, final_message: str):
    """
    Wait for a web page to answer

    :param url: the url of the web page
    :type url: str

    :param waiting_message: this message will pop up every minute
    :type waiting_message: str

    :param final_message: this message will pop up when the connection is stable
    :type final_message: str

    .. info :: if you add `%d` in your messages you can include time count in it

    .. warning :: Raise a MaxRetryError if the server has not answered after 10s
    """
    count = 0
    server_started = False
    while not server_started:
        if count == 10:
            raise MaxRetryError(url, None)
        try:
            get(url)
            server_started = True
        except (RequestsConnectionError, MaxRetryError) as _:
            sleep(1)
            logger.info(waiting_message, count)
            count += 1
    logger.info(final_message, count)


def wait_server_close(url: str, waiting_message: str, final_message: str):
    """
    Wait for a server to close

    :param url: the url to close the server
    :type url: str

    :param waiting_message: this message will pop up every minute
    :type waiting_message: str

    :param final_message: this message will pop up when the connection is down
    :type final_message: str

    .. info :: if you add `%d` in your messages you can include time count in it

    .. warning :: Raise a MaxRetryError if the server has not closed after 10s
    """
    count = 0
    server_started = False
    while not server_started:
        if count == 10:
            raise MaxRetryError(url, None)
        try:
            get(url)
            sleep(1)
            logger.info(waiting_message, count)
            count += 1
        except (RequestsConnectionError, MaxRetryError) as _:
            server_started = True
    logger.info(final_message, count)
