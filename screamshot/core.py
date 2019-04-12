from pyppeteer import launch


class ScreenShot(object):

    def __init__(self, url, method, width=None, height=None, im_type='png',
                 selector=None, wait_for=None, fully_charged=False, render=False, data=None):
        assert isinstance(url, str), 'url parameter must be a string'
        self.url = url

        assert (method == 'POST' or method == 'GET'), 'method must be equal to POST or GET'
        self.method = method

        if width:
            assert (isinstance(width, int) and width >= 0), 'width must be a positive integer'
            self.width = width

        if height:
            assert (isinstance(height, int) and height >= 0), 'height must be a positive integer'
            self.height = height

        assert (im_type == 'png' or im_type == 'jpeg'), 'im_type must be equal to png or jpeg'
        self.im_type = im_type

        if selector:
            assert isinstance(selector, str), 'selector must be a string'
            self.selector = selector

        if wait_for:
            assert isinstance(wait_for, str), 'wait_for must be a string'
            self.wait_for = wait_for
        
        assert isinstance(fully_charged, bool), 'fully_charged must be a boolean'
        self.fully_charged = fully_charged

        assert isinstance(render, bool), 'render must be a boolean'
        self.render = render

        if data:
            assert isinstance(data, str), 'data must be a string'
        self.data = data
    
    async def _init_page(self, browser):
        page = await browser.newPage()

        page_params = dict()
        if self.width:
            page_params.update({'width': self.width})
        if self.height:
            page_params.update({'height': self.height})
        page.setViewport(page_params)

        await page.goto(self.url)

        return page

    async def _selector_manager(self, page):
        if self.wait_for:
            await page.waitForSelector(self.wait_for)
        if self.selector:
            return page.querySelector(self.selector)
        return page

    async def _take_screenshot(self, element):
        screenshot_params = {'type': self.im_type}
        return element.screenshot(screenshot_params)

    async def take(self):
        browser = await launch(headless=True)
        page = await self._init_page(browser)
        element = await self._selector_manager(page)
        img = self._take_screenshot(element)
        return img
