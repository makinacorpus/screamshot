"""
Collection of functions.
"""
import logging
import asyncio
from os import remove

from pyppeteer import launch, connect


FILENAME_ENDPOINT = "/tmp/endpointlist.txt"


logger = logging.getLogger()

logger.setLevel(logging.WARNING)

formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


def to_sync(fun):
    """
    This synchronous function execute and returns the result of an asynchronous function

    :param fun: mandatory, the asynchronous function
    :type fun: function

    .. warning :: This function uses `asyncio` package
    """
    return asyncio.get_event_loop().run_until_complete(fun)


def url_match(url1, url2):
    """
    This function takes two urls and check if they are the same modulo '/' at the end
    :param url1: mandatory, the first url
    :type url1: str

    :param url2: mandatory, the second url
    :type url2: str

    :rtype: Boolean
    """
    return url1 == url2 or url1[:-1] == url2 or url1 == url2[:-1] or url1[:-1] == url2[:-1]


def set_endpoint(ws_endpoint):
    """
    This function store the web socket endpoint of the launched browser

    :param ws_endpoint: mandatory, the web socket endpoint
    :type ws_endpoint: str

    .. note :: ws_endpoint is saved in FILENAME_ENDPOINT
    """
    with open(FILENAME_ENDPOINT, "w") as ws_file:
        ws_file.write(ws_endpoint + "\n")


def get_endpoint():
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
        logger.error(str(FILENAME_ENDPOINT + " not found"))
        exit(-1)


async def open_browser(is_headless, write_websocket=True):
    """
    Launch a browser and writes its websocket endpoint in FILENAME_ENDPOINT if needed

    :param is_headless: mandatory, should the browser be launched in headless mode ?
    :type is_headless: bool

    :param write_websocket: optional, should we store the websocket endpoint in FILENAME_ENDPOINT ?
    :type write_websocket: bool

    :return: the opened browser
    :retype: pyppeteer Browser
    """
    browser = await launch(headless=is_headless, autoClose=False)
    if write_websocket:
        endpoint = browser.wsEndpoint
        set_endpoint(endpoint)
    return browser


async def close_browser(ws_endpoint):
    """
    Closes the browser related to ws_endpoint and remove FILENAME_ENDPOINT

    :param ws_endpoint: mandatory, the websocket endpoint to close
    :type ws_endpoint: str
    """
    browser = await connect(browserWSEndpoint=ws_endpoint)
    await browser.close()
    remove(FILENAME_ENDPOINT)


async def get_browser(is_headless=True):
    """
    Returns a already creatred browser if one exists or a new one if not

    :param is_headless: optionnal, should the browser be launched in headless mode ?
    :type is_headless: bool

    :retype: pyppeteer.browser.Browser
    """
    endpoint = get_endpoint()
    if endpoint:
        return await connect(browserWSEndpoint=endpoint)
    else:
        return await open_browser(is_headless)


def get_browser_sync(is_headless=True):
    """
    Same as get_browser in synchronous mode
    """
    return to_sync(get_browser(is_headless))


async def goto_page(url, browser, wait_for=None, wait_until="load"):
    """
    Checks if a page already exists in a browser or create a new one
    :param url: the url of the page to go to
    :type url: str

    :param browser: the browser to create the page into
    :type browser: browser from pyppeteer

    :param wait_for: optionnal, CSS3 selector, item to wait before handing over the page
    :type wait_for: str

    :param wait_until: optionnal, define how long you wait for the page to be loaded should be either load, domcontentloaded, networkidle0 or networkidle2
    :type wait_until: str or list(str)

    :retype: pyppeteer.page.Page
    """
    page = None

    if wait_until != "load":
        page = await browser.newPage()
        await page.goto(url, waitUntil=wait_until)
    else:
        already_created_pages = await browser.pages()
        for page_created in already_created_pages:
            if url_match(page_created.url, url):
                page = page_created
                break
        if not page:
            page = await browser.newPage()
            await page.goto(url)

    if wait_for:
        await page.waitForSelector(wait_for)

    return page


def goto_page_sync(url, browser, wait_for=None, wait_until="load"):
    """
    Same as goto_page in synchronous mode
    """
    return to_sync(goto_page(url, browser, wait_for, wait_until))
