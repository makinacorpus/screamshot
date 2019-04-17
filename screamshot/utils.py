"""
Collection of functions.
"""
import asyncio
from os import remove

from pyppeteer import launch, connect


FILENAME_ENDPOINT = "/tmp/endpointlist.txt"


def to_sync(fun):
    """
    This synchronous function execute and returns the result of an asynchronous function

    :param fun: mandatory, the asynchronous function
    :type fun: function

    .. warning :: This function uses `asyncio` package
    """
    return asyncio.get_event_loop().run_until_complete(fun)


def set_endpoint(ws_endpoint):
    """
    This function store the web socket endpoint of the launched browser

    :param ws_endpoint: mandatory, the web socket endpoint
    :type ws_endpoint: str

    .. note :: ws_endpoint is saved in $FILENAME_ENDPOINT
    """
    with open(FILENAME_ENDPOINT, "w") as ws_file:
        ws_file.write(ws_endpoint + "\n")


def get_endpoint():
    """
    This function returns the web socket endpoint of the running browser

    :retype: str

    .. note :: ws_endpoint is retrieved from $FILENAME_ENDPOINT
    """
    try:
        with open(FILENAME_ENDPOINT, "r") as ws_file:
            line = ws_file.readline()
            line = line.split()[0]
            return line
    except FileNotFoundError:
        print(FILENAME_ENDPOINT + " not found")
        return None


async def open_browser(is_headless):
    """
    Launch a browser and writes its websocket endpoint in $FILENAME_ENDPOINT

    :param is_headless: mandatory, should the browser be launched in headless mode ?
    :type is_headless: bool

    :return: the web socket endpoint
    :retype: str
    """
    browser = await launch(headless=is_headless, autoClose=False)
    endpoint = browser.wsEndpoint
    set_endpoint(endpoint)
    return endpoint


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
    return await open_browser(is_headless)


# Check if the browser already have the page and then go to the page
async def goto_page(url, browser, params):
    """
    Checks if a page already exists in a browser or create a new one

    :param url: the url of the page to go to
    :type url: str

    :param browser: the browser to create the page into
    :type browser: browser from pyppeteer

    :param params: the parameters of pyppeteer to create a browser
    :type params: dict

    :retype: pyppeteer.page.Page
    """
    page = None
    wait_until = params.get('wait_until')
    if wait_until:
        page = await browser.newPage()
        await page.goto(url, waitUntil=wait_until)
    else:
        for page_created in browser.pages():
            if page_created.url == url:
                page = page_created
                break
        if not page:
            page = await browser.newPage()
            await page.goto(url)

    wait_for = params.get('wait_for')
    if wait_for:
        await page.waitForSelector(wait_for)

    arg_viewport = params.get('arg_viewport')
    if arg_viewport:
        await page.setViewport(arg_viewport)

    return page
