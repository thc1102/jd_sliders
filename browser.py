from playwright.async_api import async_playwright


class MyBrowser:
    """
    自动化操作浏览器 管理类
    """

    def __init__(self):
        self.browser = None
        self.playwright = None

    async def new_browser(self, headless=True):
        """
        初始化browser
        :param headless: 是否开启无头模式
        """
        if self.playwright is None:
            self.playwright = await async_playwright().start()
        self.browser = browser = await self.playwright.chromium.launch(headless=headless)

    async def new_context(self, headless=True):
        """
        初始化context(移动端自定义的配置)
        :param headless: 是否开启无头模式
        :return: context context
        """
        if self.browser is None:
            await self.new_browser(headless)
        context = await self.browser.new_context(
            locale='zh-CN',
            geolocation={'longitude': 116.39014, 'latitude': 39.913904},
            permissions=['geolocation'],
            color_scheme='light',
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 15_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Mobile/15E148 Safari/604.1',
            viewport={'width': 390, 'height': 844},
            device_scale_factor=3,
            is_mobile=True,
            has_touch=True
        )
        return context

    async def new_page(self, context=None):
        """
        初始化new_page
        :param context: 初始化的context
        :return: page
        """
        if context is None:
            page = await self.browser.new_page()
        else:
            page = await context.new_page()
        return page

    async def close(self):
        await self.browser.close()
        await self.playwright.stop()
