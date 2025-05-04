"""
@package base

Base Page class implementation
It implements methods which are common to all the pages throughout the application

This class needs to be inherited by all the page classes
This should not be used by creating object instances

Example:
    Class LoginPage(BasePage)
"""
from base.playwright_driver import PlaywrightDriver
from utils.util import Util

class BasePage(PlaywrightDriver):

    def __init__(self, page):
        """
        Inits BasePage class

        Returns:
            None
        """
        self.page = page
        self.util = Util()