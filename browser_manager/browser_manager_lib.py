from pyppeteer import connect

from browser_opener_closer_script import get_endpoints, open_browser, to_sync


# Return a list of available browsers
def get_browser_list(is_headless=True):
    endpoint_list = get_endpoints()
    if endpoint_list:
        browser_list = []
        for endpoint in endpoint_list:
            browser_list.append(connect(browserWSEndpoint=endpoint))
    else:
        browser_list = [to_sync(open_browser(is_headless))]
    return browser_list


# Return the first browser (can be tuned in the future)
def get_browser(is_headless=True):
    return get_browser_list(is_headless)[0]


async def goto_page_async(url, params):
    browser = get_browser()
    page = None
    for page_created in browser.pages():
        if page_created.url == url:
            page = page_created
            break
    if not page:
        page = await browser.newPage()

    arg_viewport = params.get('arg_viewport')
    if arg_viewport:
        await page.setViewport(arg_viewport)

    wait_until = params.get('wait_until')
    if wait_until:
        await page.goto(url, waitUntil=wait_until)
    else:
        await page.goto(url)
    return page


def goto_page(url, params):
    return to_sync(goto_page_async(url, params))
