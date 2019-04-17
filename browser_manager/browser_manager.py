from browser_opener_closer_script import get_endpoints, open_browser, to_sync

from pyppeteer import connect


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
