"""
generate_bytes_img and generate_bytes_img_prom functions.
"""
from typing import Any
from asyncio import get_event_loop, ensure_future, Future

from pyppeteer.page import Page
from pyppeteer.browser import Browser

from screamshot.utils import get_browser


def _parse_parameters(**kwargs) -> dict:
    arg_viewport = {}
    if "width" in kwargs:
        arg_viewport.update({"width": kwargs.pop("width")})
    if "height" in kwargs:
        arg_viewport.update({"height": kwargs.pop("height")})

    if "wait_until" in kwargs:
        wait_until = kwargs.pop("wait_until")
        if not isinstance(wait_until, list):
            wait_until = [wait_until]
    else:
        wait_until = ["load"]

    screenshot_options = {"fullPage": kwargs.get("full_page", False)}
    if "path" in kwargs:
        path = kwargs.pop("path")
        screenshot_options.update({"path": path})

    selector = None
    if "selector" in kwargs:
        selector = kwargs.pop("selector")

    wait_for = None
    if "wait_for" in kwargs:
        wait_for = kwargs.pop("wait_for")

    credentials = {}
    if 'credentials' in kwargs:
        credentials_data = kwargs.pop('credentials')
        if credentials_data:
            if 'username' in credentials_data and 'password' in credentials_data:
                credentials['login'] = True
            if 'token_in_header' in credentials_data:
                credentials['token_in_header'] = credentials_data.pop('token_in_header')
            credentials.update({'credentials_data': credentials_data})

    return {
        "arg_viewport": arg_viewport,
        "screenshot_options": screenshot_options,
        "selector": selector,
        "wait_for": wait_for,
        "wait_until": wait_until,
        "credentials": credentials,
    }


async def _page_manager(browser: Browser, url: str, params: dict) -> Page:
    page = await browser.newPage()

    arg_viewport = params.get("arg_viewport")
    if arg_viewport:
        await page.setViewport(arg_viewport)

    credentials = params.get("credentials")
    if credentials:
        credentials_data = credentials.get("credentials_data")
        if credentials.get("login"):
            await page.authenticate(credentials_data)
        if credentials.get("token_in_header"):
            await page.setExtraHTTPHeaders(credentials_data)

    await page.goto(url, waitUntil=params.get("wait_until"))

    wait_for = params.get("wait_for")
    if wait_for:
        await page.waitForSelector(wait_for)

    return page


async def _selector_manager(page: Page, params: dict) -> Any:
    selector = params.get("selector")
    if selector:
        return await page.querySelector(selector)

    return page


async def generate_bytes_img(url: str, **kwargs) -> bytes:
    """
    This function takes a screenshot and returns it as a `bytes` object

    :param url: mandatory, the website's url
    :type url: str

    :param path: optional, the path to the image output
    :type path: str

    :param credentials: If the website uses "login authentication", you can specify two fields: \
        `username` and `password`. Otherwise, if it uses a "token identification" that must be \
            specified in the header, please indicate into `credentials` the field that should be \
                passed to the header, as well as a `token_in_header` field equal to `True`.
    :type credentials: dict

    :param width: optionnal, the window's width
    :type width: int

    :param height: optionnal, the window's height
    :type height: int

    :param selector: optionnal, CSS3 selector, item whose screenshot is taken
    :type selector: str

    :param wait_for: optionnal, CSS3 selector, item to wait before taking the screenshot
    :type wait_for: str

    :param wait_until: optionnal, define how long you wait for the page to be loaded should \
        be either load, domcontentloaded, networkidle0 or networkidle2
    :type wait_until: str or list(str)

    :returns: the binary code of the image
    :retype: `bytes`

    .. warning:: It uses **pyppeteer** and so **async** functions

    .. note :: The `asyncio` library can be used to manipulate this function

    :Exemple:

    .. code-block:: python

        import asyncio

        from screamshot import generate_bytes_img


        async def main():
            img = await generate_bytes_img('https://makina-corpus.com/expertise/cartographie',
                                    selector='.image-right', wait_until='networkidle0')
            print(img)


        if __name__ == '__main__':
            asyncio.get_event_loop().run_until_complete(main())
    """
    params = _parse_parameters(**kwargs)

    browser = await get_browser()

    page = await _page_manager(browser, url, params)

    element = await _selector_manager(page, params)

    image = await element.screenshot(options=params.get("screenshot_options"))

    await page.close()
    return image


async def generate_bytes_img_prom(url: str, future: Future, **kwargs):
    """
    This function takes a screenshot and returns it as a `bytes` object in the promise given in \
        the parameters

    :param url: mandatory, the website's url
    :type url: str

    :param future: mandatory, a promise
    :type future: `asyncio.Future`

    :param path: optional, the path to the image output
    :type path: str

    :param credentials: If the website uses "login authentication", you can specify two fields: \
        `username` and `password`. Otherwise, if it uses a "token identification" that must be \
            specified in the header, please indicate into `credentials` the field that should be \
                passed to the header, as well as a `token_in_header` field equal to `True`.
    :type credentials: dict

    :param width: optionnal, the window's width
    :type width: int

    :param height: optionnal, the window's height
    :type height: int

    :param selector: optionnal, CSS3 selector, item whose screenshot is taken
    :type selector: str

    :param wait_for: optionnal, CSS3 selector, item to wait before taking the screenshot
    :type wait_for: str

    :param wait_until: optionnal, define how long you wait for the page to be loaded should \
        be either load, domcontentloaded, networkidle0 or networkidle2
    :type wait_until: str or list(str)

    :retype: None

    .. warning:: It uses **pyppeteer** and so **async** functions

    .. warning:: This function must be used with the `asyncio` library

    :Exemple:

    .. code-block:: python

        # views.py in a Django project
        import asyncio

        from django.http import HttpResponse

        from screamshot import generate_bytes_img_prom


        def home(request):
            loop = asyncio.get_event_loop()
            future = asyncio.Future()

            asyncio.ensure_future(
                generate_bytes_img_prom('https://www.google.fr', future))
            loop.run_until_complete(future)

            print(futur.result())
            return HttpResponse('Done')
    """
    img = await generate_bytes_img(url, **kwargs)

    future.set_result(img)


def generate_bytes_img_django_wrap(url: str, **kwargs):
    """
    This function takes a screenshot and returns it as a `bytes` object in \
        synchorouns mode, usable directly in django

    :param url: mandatory, the website's url
    :type url: str

    :param path: optional, the path to the image output
    :type path: str

    :param width: optionnal, the window's width
    :type width: int

    :param height: optionnal, the window's height
    :type height: int

    :param selector: optionnal, CSS3 selector, item whose screenshot is taken
    :type selector: str

    :param wait_for: optionnal, CSS3 selector, item to wait before taking the screenshot
    :type wait_for: str

    :param wait_until: optionnal, define how long you wait for the page to be loaded should \
        be either load, domcontentloaded, networkidle0 or networkidle2
    :type wait_until: str or list(str)

    :returns: the binary code of the image
    :retype: `bytes`


    """

    loop = get_event_loop()
    future = Future() #type: Future

    ensure_future(generate_bytes_img_prom(url, future, **kwargs))
    loop.run_until_complete(future)

    return future.result()
