"""
generate_bytes_img and generate_bytes_img_prom functions
"""
from os import environ

from pyppeteer import launch, connect


# Name of the envrinment variable which contains the chrome ws endpoint
VENV = 'WS_ENDPOINT_SCREAMSHOT'


def _parse_parameters(**kwargs):
    arg_viewport = {}
    if 'width' in kwargs:
        arg_viewport.update({'width': kwargs.pop('width')})
    if 'height' in kwargs:
        arg_viewport.update({'height': kwargs.pop('height')})

    wait_until = None
    if 'wait_until' in kwargs:
        wait_until = kwargs.pop('wait_until')
        if not isinstance(wait_until, list):
            wait_until = [wait_until]

    return {
        'arg_viewport': arg_viewport,
        'full_page': kwargs.get('full_page', False),
        'selector': kwargs.get('selector'),
        'wait_for': kwargs.get('wait_for'),
        'wait_until': wait_until,
    }


async def _init_browser():
    browser_ws_endpoint = environ.get(VENV)
    if browser_ws_endpoint:
        browser = await connect({'browserWSEndpoint': browser_ws_endpoint})
        return browser
    browser = await launch(options={'headless': True})
    return browser


async def _init_page(url, browser, params):
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


async def _selector_manager(page, params):
    wait_for = params.get('wait_for')
    if wait_for:
        await page.waitForSelector(wait_for)

    selector = params.get('selector')
    if selector:
        return await page.querySelector(selector)
    return page


async def generate_bytes_img(url, **kwargs):
    """
    This function takes a screenshot and returns it as a `bytes` object

    :param url: mandatory, the website's url
    :type url: str

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

    browser = await _init_browser()

    page = await _init_page(url, browser, params)

    element = await _selector_manager(page, params)

    screamshot_params = {'fullPage': params.get('full_page')}
    image = await element.screenshot(screamshot_params)

    return image


async def generate_bytes_img_prom(url, future, **kwargs):
    """
    This function takes a screenshot and returns it as a `bytes` object in the promise given in \
        the parameters

    :param url: mandatory, the website's url
    :type url: str

    :param future: mandatory, a promise
    :type future: `asyncio.Future`

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