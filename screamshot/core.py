import asyncio

from pyppeteer import launch


WAIT_UNTIL_POSSIBLE_VALUES = ['load', 'domcontentloaded', 'networkidle0', 'networkidle2']


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


def _check_params(url, params):
    assert isinstance(url, str), 'url parameter must be a string'


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

    :returns: the base64 code of the image
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

    browser = await launch(headless=True)

    page = await _init_page(url, browser, params)

    element = await _selector_manager(page, params)

    screamshot_params = {'fullPage': params.get('full_page')}
    image = await element.screenshot(screamshot_params)

    await browser.close()
    return image


async def generate_bytes_img_prom(url, future, **kwargs):
    """
    This function takes a screenshot

    :param url: mandatory, the website's url
    :type url: str

    :param check_params: optionnal, default True, allows the verification of parameters
    :type check_params: bool

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

    :returns: (`bytes`) the base64 code of the image

    :raises AssertionError: this exception is raised if a parameter do not respect the documentation

    .. note:: If `check_params` is equal to `True` and if a parameter does not respect the \
        conditions, the function raises an `AssertionError`

    .. warning:: It uses **pyppeteer** and so **async** functions

    :Exemple:

    .. code-block:: python

        from screamshot import generate_bytes_img
        def main():
            img = generate_bytes_img('https://makina-corpus.com/expertise/cartographie',
                                    selector='.image-right', wait_until='networkidle0')
            print(img)
        if __name__ == '__main__':
            main()
    """
    img = await generate_bytes_img(url, **kwargs)
    future.set_result(img)
