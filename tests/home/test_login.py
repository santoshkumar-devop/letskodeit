from pages.home.login_page import LoginPage
import pytest
from utils.teststatus import _TestExecutionStatus


@pytest.mark.usefixtures("oneTimeSetUp")
class TestLogin:

    @pytest.fixture(autouse=True)
    def classSetup(self):
        self.lp = LoginPage(self.page)
        self.ts = _TestExecutionStatus(self.page)

    def test_invalid_login(self):
        self.lp.login("test@email.com", "abcabcde")
        self.lp.verifyLoginUnsuccessful()

    def test_valid_login(self):
        self.lp.login("test@email.com", "abcabc")
        result1 = self.lp.verifyHomePageTitle()
        self.ts.mark(result1, "Title Verified")
        result2 = self.lp.verifyLoginSuccessful()
        self.ts.markFinal("test_validLogin", result2, "Login was successful")
        self.lp.logout()



