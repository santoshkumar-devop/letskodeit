from base.playwright_driver import PlaywrightDriver
from pages.home.navigation_page import NavigationPage

class LoginPage(PlaywrightDriver):
    def __init__(self, page):
        super().__init__(page)
        self.nav = NavigationPage(page)

    # Locators
    _login_link = "//a[normalize-space()='Sign In']"
    _email_field = "//input[@placeholder='Email Address']"
    _password_field = "//input[@placeholder='Password']"
    _login_button = "//button[@id='login']"
    _my_courses_link = "//h1[contains(text(),'My Courses')]"
    _login_error_message = "//span[@id='incorrectdetails' and contains(., 'Incorrect login details')]"
    _expected_title = "My Courses"
    _logout_link = "//a[@href='/logout']"


    # Actions

    def clickLoginLink(self):
        self.elementClick("xpath", self._login_link)

    def enterEmail(self, email):
        self.sendKeys("xpath", self._email_field, email)

    def enterPassword(self, password):
        self.sendKeys("xpath", self._password_field, password)

    def clickLoginButton(self):
        self.elementClick("xpath", self._login_button)

    def clearEmail(self):
        self.clearField("xpath", self._email_field)

    def clearPassword(self):
        self.clearField("xpath", self._password_field)

    def login(self, email="", password=""):
        self.clickLoginLink()
        self.clearEmail()
        self.enterEmail(email)
        self.clearPassword()
        self.enterPassword(password)
        self.clickLoginButton()

    def verifyHomePageTitle(self):
        result = self.expect_title(self._expected_title)
        return result

    def verifyLoginSuccessful(self):
        result = self.expect_element_visible("xpath", self._my_courses_link)
        return result

    def verifyLoginUnsuccessful(self):
        self.expect_element_visible("xpath", self._login_error_message)

    def logout(self):
        self.nav.navigateToUserSettings()
        self.elementClick("xpath", self._logout_link)

