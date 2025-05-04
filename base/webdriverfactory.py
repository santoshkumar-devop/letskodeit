from playwright.sync_api import sync_playwright

class WebDriverFactory:
    def __init__(self, browser_name, headless=False):
        """
        Initialize the WebDriverFactory with browser name and headless mode.
        :param browser_name: Name of the browser ('chromium', 'firefox', 'webkit').
        :param headless: Boolean to run browser in headless mode.
        """
        self.browser_name = browser_name
        self.headless = headless
        self.playwright = None
        self.browser = None

    def getWebDriverInstance(self):
        """
        Launch the browser, navigate to the base URL, and return the page instance.
        :param base_url: The URL to navigate to.
        :return: Playwright page instance.
        """
        base_url = "https://www.letskodeit.com/"
        # Start playwright
        self.playwright = sync_playwright().start()

        # Launch the specified browser
        if self.browser_name == "chromium":
            self.browser = self.playwright.chromium.launch(headless=self.headless)
        elif self.browser_name == "firefox":
            self.browser = self.playwright.firefox.launch(headless=self.headless)
        elif self.browser_name == "edge":
            self.browser = self.playwright.webkit.launch(headless=self.headless)
        else:
            raise ValueError(f"Unsupported browser: {self.browser_name}")

        # Create a new page
        context = self.browser.new_context()
        page = context.new_page()

        # Navigate to the base URL
        page.goto(base_url)
        return page

    def close(self):
        """
        Close the browser and stop playwright.
        This method should be called when you're done using the WebDriverFactory.
        """
        if self.browser:
            self.browser.close()
            self.browser = None

        if self.playwright:
            self.playwright.stop()
            self.playwright = None