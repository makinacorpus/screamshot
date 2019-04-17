from os import remove
import asyncio
from pyppeteer import launch, connect


FILENAME_ENDPOINT = "endpointlist.txt"


# Set an async function to synchronous mode using asyncio
def to_sync(fun):
    return asyncio.get_event_loop().run_until_complete(fun)


# Write the websocket endpoint into the file
def set_endpoint(ws_endpoint):
    with open(FILENAME_ENDPOINT, "a") as ws_file:
        ws_file.write(ws_endpoint + "\n")
    return ws_endpoint


# Read the file to get the ws endpoints and return them into a list of string
def get_endpoints():
    endpoint_list = []
    try:
        with open(FILENAME_ENDPOINT, "r") as ws_file:
            for line in ws_file:
                line = line.split()[0]
                endpoint_list.append(line)
        return endpoint_list
    except FileNotFoundError:
        print(FILENAME_ENDPOINT + " not found")
        return None


# Launch a browser which will be closed only when delete_browser(ws_endpoint_list) is called
async def open_browser(is_headless):
    browser = await launch(headless=is_headless, autoClose=False)
    endpoint = browser.wsEndpoint
    set_endpoint(endpoint)
    return endpoint


# Close all the browsers in the ws_endpoint_list
async def delete_browser(ws_endpoint_list):
    if ws_endpoint_list:
        for ws_endpoint in ws_endpoint_list:
            browser = await connect(browserWSEndpoint=ws_endpoint)
            await browser.close()
        remove(FILENAME_ENDPOINT)


# Return a list of available browsers
async def get_browser_list_async(is_headless=True):
    endpoint_list = get_endpoints()
    if endpoint_list:
        browser_list = []
        for endpoint in endpoint_list:
            browser_list.append(await connect(browserWSEndpoint=endpoint))
    else:
        browser_list = [await open_browser(is_headless)]
    return browser_list


def get_browser_list(is_headless=True):
    return to_sync(get_browser_list_async(is_headless))


# Return the first browser (can be tuned in the future)
async def get_browser_async(is_headless=True):
    return await get_browser_list_async(is_headless)[0]


def get_browser(is_headless=True):
    return get_browser_list(is_headless)[0]


# Check if the browser already have the page and then go to the page
async def goto_page_async(url, browser, params):
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

    arg_viewport = params.get('arg_viewport')
    if arg_viewport:
        await page.setViewport(arg_viewport)

    return page


def goto_page(url, browser, params):
    return to_sync(goto_page_async(url, browser, params))
