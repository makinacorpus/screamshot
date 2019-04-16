import asyncio

from pyppeteer import launch


WAIT_UNTIL_POSSIBLE_VALUES = ['load', 'domcontentloaded', 'networkidle0', 'networkidle2']


def _check_list_type(list_to_check, expected_type):
    return (bool(list_to_check)
            and all(isinstance(elem, expected_type) for elem in list_to_check))


def _check_list_of_str_value(list_to_check, values):
    if isinstance(list_to_check, str):
        list_to_check = [list_to_check]
    return all([e in values for e in list_to_check])


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

    arg_viewport = params.get('arg_viewport')
    if arg_viewport:
        height = arg_viewport.get('height')
        width = arg_viewport.get('width')
        assert height and width, 'both height and width must be define or none of them'
        assert (isinstance(height, int) and height >= 0), 'height must be a positive integer'
        assert (isinstance(width, int) and width >= 0), 'width must be a positive integer'

    selector = params.get('selector')
    if selector:
        assert isinstance(selector, str), 'selector must be a string'

    wait_for = params.get('wait_for')
    if wait_for:
        assert isinstance(wait_for, str), 'wait_for must be a string'

    wait_until = params.get('wait_until')
    if wait_until:
        assert (_check_list_type(wait_until, str)
                and _check_list_of_str_value(
                    wait_until, WAIT_UNTIL_POSSIBLE_VALUES)), (
                        'wait_until should be a string or a list of string of load,'
                        + ' domcontentloaded, networkidle0 or networkidle2')


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


async def _generate_bytes_img(url, check_params, **kwargs):
    params = _parse_parameters(**kwargs)
    if check_params:
        _check_params(url, params)

    browser = await launch(headless=True)

    page = await _init_page(url, browser, params)

    element = await _selector_manager(page, params)

    screamshot_params = {'fullPage': params.get('full_page')}
    image = await element.screenshot(screamshot_params)

    await browser.close()
    return image


def generate_bytes_img(url, check_params=True, **kwargs):
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
    return asyncio.get_event_loop().run_until_complete(_generate_bytes_img(url, check_params,
                                                                           **kwargs))
