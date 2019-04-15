import asyncio

from pyppeteer import launch


class ScreenShot():
    """
    This object allows a user to take a web page screenshot

    Attributes:
    * url, mandatory, str, the website's url
    * width, optionnal, positive int, the window's width
    * height, optionnal, positive int, the window's height
            If fullPage is True, width and height can only increase the size on the image.

    * img_type, optionnal, png (default) or jpeg, the image type
    * selector, optionnal, CSS3 selector, item whose screenshot is taken
    * wait_for, optionnal, CSS3 selector, item to wait before taking the screenshot
    * wait_until, optionnal, string or list of string, default None, define how long you wait
      for the page to be loaded should be either load, domcontentloaded, networkidle0 or
      networkidle2
    * render, optionnal, boolean, default False, generate an html page
    * data, optionnal, str, the html page generated. Must contains ${screenshot}.
    * fullPage, optionnal, boolean (default False), do we take a screamshot of the whole scrollable page ?

    Methods:
    * load, () => void'', load the page
    * screamshot, () => image, take a screamshot
    * load_and_screamshot, () => image, load the page and take a screamshot
    
    """

    wait_until_possible_values = ['load', 'domcontentloaded', 'networkidle0', 'networkidle2']

    @staticmethod
    def _check_list_type(list_to_check, expected_type):
        return (bool(list_to_check)
                and all(isinstance(elem, expected_type) for elem in list_to_check))

    @staticmethod
    def _check_list_of_str_value(list_to_check, values):
        if isinstance(list_to_check, str):
            list_to_check = [list_to_check]
        return all([e in values for e in list_to_check])

    def __init__(self, url, **kwargs):

        # Initialising attributes
        self.browser = None
        self.page = None

        assert isinstance(url, str), 'url parameter must be a string'
        self.url = url

        # We need both height and width or none of them, so if we only have one, we set the other
        # one to a default value.
        # If we have none of them, we set argViewport to None

        self.arg_viewport = {}
        if 'height' in kwargs:
            height = kwargs.pop('height')
            assert (isinstance(height, int) and height >= 0), 'height must be a positive integer'
            self.arg_viewport.update({'height': height})
        else:
            self.arg_viewport.update({'height': 600})
        if 'width' in kwargs:
            width = kwargs.pop('width')
            assert (isinstance(width, int) and width >= 0), 'height must be a positive integer'
            self.arg_viewport.update({'height': width})
        else:
            self.arg_viewport.update({'width': 800})

        self.full_page = None
        if 'full_page' in kwargs:
            full_page = kwargs.pop('full_page')
            assert isinstance(full_page, bool), 'fullPage must be a boolean'
            self.full_page = full_page

        if 'selector' in kwargs:
            selector = kwargs.pop('selector')
            assert isinstance(selector, str), 'selector must be a string'
            self.selector = selector
        else:
            self.selector = None

        if 'wait_for' in kwargs:
            wait_for = kwargs.pop('wait_for')
            assert isinstance(wait_for, str), 'wait_for must be a string'
            self.wait_for = wait_for
        else:
            self.wait_for = None

        self.wait_until = None
        if 'wait_until' in kwargs:
            wait_until = kwargs.pop('wait_until')
            assert (self._check_list_type(wait_until, str)
                    and self._check_list_of_str_value(
                        wait_until, self.wait_until_possible_values)), (
                            'wait_until should be a string or a list of string of load,'
                            + ' domcontentloaded, networkidle0 or networkidle2')
            self.wait_until = wait_until

    async def _init_page(self, browser):
        page = await browser.newPage()
        if self.arg_viewport:
            await page.setViewport(self.arg_viewport)

        if self.wait_until:
            await page.goto(self.url, waitUntil=self.wait_until)
        else:
            await page.goto(self.url)

        return page

    async def _selector_manager(self):
        if self.wait_for:
            await self.page.waitForSelector(self.wait_for)
        if self.selector:
            return await self.page.querySelector(self.selector)
        return self.page

    async def _load(self):
        self.browser = await launch()
        self.page = await self._init_page(self.browser)
    
    def load(self):
        asyncio.get_event_loop().run_until_complete(self._load())
    
    async def _screamshot(self):
        element = await self._selector_manager()
        screamshot_params = {'fullPage': self.full_page}
        image = await element.screenshot(screamshot_params)
        return image

    def screamshot(self):
        return asyncio.get_event_loop().run_until_complete(self._screamshot())

    async def _load_and_screamshot(self):
        await self._load()
        image = await self._screamshot()
        return image

    def load_and_screamshot(self):
        return asyncio.get_event_loop().run_until_complete(self._load_and_screamshot())
