import utils.custom_logger as cl
import logging
from base.playwright_driver import PlaywrightDriver


class NavigationPage(PlaywrightDriver):

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, page):
        super().__init__(page)
        self.page = page

    # Locators
    _my_courses = "//a[normalize-space()='MY COURSES']"
    _all_courses_link = "//a[normalize-space()='ALL COURSES']"
    _practice = "//a[normalize-space()='PRACTICE']"
    _user_settings_icon = "//button[@id='dropdownMenu1']//a[@class='dynamic-link']"


    def navigateToAllCourses(self):
        self.elementClick("xpath", locator=self._all_courses_link)

    def navigateToMyCourses(self):
        self.elementClick("xpath", locator=self._my_courses)

    def navigateToPractice(self):
        self.elementClick("xpath", locator=self._practice)

    def navigateToUserSettings(self):
        userSettingsElement = self.waitForElement("xpath", locator=self._user_settings_icon)
        self.elementClick(locator=self._user_settings_icon,
                                      locatorType="xpath")