import asyncio
from os import remove

from pyppeteer import launch, connect


FILENAME_ENDPOINT = "/tmp/endpointlist.txt"


def to_sync(fun):
    """
    This function returns the result of await fun
    :param fun: mandatory, the function to be awaited
    :type fun: function to be awaited
    """
    return asyncio.get_event_loop().run_until_complete(fun)


def set_endpoint(ws_endpoint):
    """
    This function writes the endpoint to the file FILENAME_ENDPOINT
    :param ws_endpoint: the endpoint to be written
    :type ws_endpoint: str
    """
    with open(FILENAME_ENDPOINT, "w") as ws_file:
        ws_file.write(ws_endpoint + "\n")


def get_endpoint():
    """
    This function returns the endpoint into a string if FILENAME_ENDPOINT exists, \
        None if it does not
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
    Launch a browser and writes its websocket endpoint in FILENAME_ENDPOINT
    :param is_headless: should the browser be launched in headless mode ?
    :type is_headless: bool
    """
    browser = await launch(headless=is_headless, autoClose=False)
    endpoint = browser.wsEndpoint
    set_endpoint(endpoint)
    return endpoint


async def close_browser(ws_endpoint):
    """
    Closes the browser related to ws_endpoint and remove FILENAME_ENDPOINT
    :param ws_endpoint: the websocket endpoint to close
    :type ws_endpoint: str
    """
    browser = await connect(browserWSEndpoint=ws_endpoint)
    await browser.close()
    remove(FILENAME_ENDPOINT)


async def get_browser(is_headless=True):
    """
    Returns a already creatred browser if one exists, a new one if not
    :param is_headless: should the browser be launched in headless mode ?
    :type is_headless: bool
    """
    endpoint = get_endpoint()
    if endpoint:
        return await connect(browserWSEndpoint=endpoint)
    return await open_browser(is_headless)


def get_browser_sync(is_headless=True):
    """
    Same as get_browser in synchronous mode
    """
    return to_sync(get_browser(is_headless))


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


def goto_page_sync(url, browser, params):
    """
    Same as goto_page in synchronous mode
    """
    return to_sync(goto_page(url, browser, params))
