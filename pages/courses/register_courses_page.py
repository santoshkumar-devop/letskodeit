from time import sleep

import utils.custom_logger as cl
import logging
from base.playwright_driver import PlaywrightDriver

class RegisterCoursesPage(PlaywrightDriver):

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, page):
        super().__init__(page)
        self.page = page

    ################
    ### Locators ###
    ################

    _search_box = "//input[@id='search']"
    _search_button = "//i[@class='fa fa-search']"
    _course = "//h4[normalize-space()='{}']"
    _enroll_button = "//button[normalize-space()='Enroll in Course']"
    _cc_num = "iframe[title='Secure card number input frame']"
    _cc_exp = "iframe[title='Secure expiration date input frame']"
    _cc_cvv = "iframe[title='Secure CVC input frame']"
    _select_country = "//select[@name='country-list']"
    _submit_enroll = "//div[@id='new_card']//button[contains(text(),'Enroll in Course')]"
    _enroll_error_message = "//span[contains(.,'Your card')]"
    _buy = "button.checkout-button:visible"

    ############################
    ### Element Interactions ###
    ############################

    def clickAllCoursesLink(self):
        self.elementClick("xpath", self._all_courses_link)

    def enterCourseName(self, name):
        self.sendKeys("xpath", self._search_box, name)

    def clickSearchButton(self):
        self.elementClick("xpath", self._search_button)

    def selectCourseToEnroll(self, fullCourseName):
        self.elementClick("xpath", self._course.format(fullCourseName))

    def clickOnEnrollButton(self):
        self.elementClick("xpath", self._enroll_button)

    def enterCardNum(self, num):
        iframe_locator = self.switchToFrame(self._cc_num)
        iframe_locator.locator("input[name='cardnumber']").fill(str(num))

    def enterCardExp(self, exp):
        expiry_frame_locator  = self.switchToFrame(self._cc_exp)
        expiry_frame_locator.locator("input[name='exp-date']").fill(exp)

    def enterCardCVV(self, cvv):
        cvc_frame_locator = self.switchToFrame(self._cc_cvv)
        cvc_frame_locator.locator("input[name='cvc']").fill(cvv)

    def selectCountry(self, country):
        self.selectElementFromDropDown("xpath", self._select_country, country)

    def clickEnrollSubmitButton(self):
        self.elementClick("xpath", self._submit_enroll)

    def clickBuyButton(self):
        self.elementClick("css", self._buy)

    def enterCreditCardInformation(self, num, exp, cvv):
        self.enterCardNum(num)
        self.enterCardExp(exp)
        self.enterCardCVV(cvv)

    def enrollCourse(self, num="", exp="", cvv=""):
        self.clickOnEnrollButton()
        self.enterCreditCardInformation(num, exp, cvv)
        self.selectCountry("India")
        self.clickBuyButton()

    def verifyEnrollFailed(self):
        result = self.expect_element_visible("xpath", self._enroll_error_message)
        return result