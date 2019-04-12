from pyppeteer import launch
from operator import xor


# If fullPage is set to True, width and height cannot reduce the size of the screenshot

class ScreenShot(object):
    """
    This object allows a user to take a web page screenshot

    Attributes:
    * url, mandatory, str, the website's url
    * width, optionnal, positive int, the window's width
    * height, optionnal, positive int, the window's height
    * img_type, optionnal, png (default) or jpeg, the image type
    * selector, optionnal, CSS3 selector, item whose screenshot is taken
    * wait_for, optionnal, CSS3 selector, item to wait before taking the screenshot
    * wait_until, optionnal, string or list of string, default None, define how long you wait for the page to be loaded should be either load, domcontentloaded, networkidle0 or networkidle2
    * render, optionnal, boolean, default False, generate an html page
    * data, optionnal, str, the html page generated. Must contains ${screenshot}.

    Methods:
    * take, () => b'', async, take a screenshot
    """

	@staticmethod
	def _checkListType(l, expected_type):
		return((bool(l) and all(isinstance(elem, expected_type) for elem in l)))

    def __init__(self, url, width=None, height=None, img_type='png',
                 selector=None, wait_for=None, wait_until=None, render=False, data=None):
        assert isinstance(url, str), 'url parameter must be a string'
        self.url = url

        if height and width:
            assert (isinstance(width, int) and width >= 0), 'width must be a positive integer'
            assert (isinstance(height, int) and height >= 0), 'height must be a positive integer'
            self.argViewport = {'width': width, 'height': height}
        elif width:
            assert (isinstance(width, int) and width >= 0), 'width must be a positive integer'
            self.argViewport = {'width': width, 'height': 600}
        elif height:
            assert (isinstance(height, int) and height >= 0), 'height must be a positive integer'
            self.argViewport = {'width': 800, 'height': height}
        else:
            self.argViewport = None
            
        assert (img_type == 'png' or img_type == 'jpeg'), 'img_type must be equal to png or jpeg'
        self.img_type = img_type

        if selector:
            assert isinstance(selector, str), 'selector must be a string'
        self.selector = selector
        
        if wait_for:
            assert isinstance(wait_for, str), 'wait_for must be a string'
        self.wait_for = wait_for
		
		if wait_until:
			assert ScreenShot._checkListType(wait_until, str), 'wait_until should be a string or a list of string'
		self.wait_until = wait_until

        assert isinstance(fully_charged, bool), 'fully_charged must be a boolean'
        self.fully_charged = fully_charged

        assert isinstance(render, bool), 'render must be a boolean'
        self.render = render

        if data:
            assert isinstance(data, str), 'data must be a string'
        self.data = data

    async def _init_page(self, browser):
        page = await browser.newPage()
        if self.argViewport:
               await page.setViewport(self.argViewport)

		if self.wait_until:
			await page.goto(self.url, waitUntil=self.wait_until)
		else:
			await page.goto(self.url)

        return page

    async def _selector_manager(self, page):
        if self.wait_for:
            await page.waitForSelector(self.wait_for)
        if self.selector:
            return page.querySelector(self.selector)

        return page

    async def _take_screenshot(self, element):
        screenshot_params = {'type': self.img_type}
        return await element.screenshot(screenshot_params)

    async def take(self):
        browser = await launch(headless=True)
        page = await self._init_page(browser)
        element = await self._selector_manager(page)
        img = await self._take_screenshot(element)
        await browser.close()
        return img
