from pages.courses.register_courses_page import RegisterCoursesPage
from pages.home.login_page import LoginPage
from utils.teststatus import _TestExecutionStatus
import pytest
from utils.read_data import getCSVData
from pages.home.navigation_page import NavigationPage

@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
class TestRegisterCourse:

    @pytest.fixture(autouse=True)
    def classSetup(self, oneTimeSetUp):
        self.courses = RegisterCoursesPage(self.page)
        self.lp = LoginPage(self.page)
        self.ts = _TestExecutionStatus(self.page)
        self.nav = NavigationPage(self.page)

    @pytest.fixture(autouse=True)
    def setUp(self):
        self.lp.login("test@email.com", "abcabc")
        self.nav.navigateToAllCourses()
        yield
        self.lp.logout()

    @pytest.mark.parametrize("course", getCSVData("E:\\Projects\\letsKodeit\\resources\\testdata.csv"))
    def test_courseEnrollment(self, course):
        self.courses.enterCourseName(course["courseName"])
        self.courses.clickSearchButton()
        self.courses.selectCourseToEnroll(course["courseName"])
        self.courses.enrollCourse(num=course["ccNum"], exp=course["ccExp"], cvv=course["ccCVV"])
        result = self.courses.verifyEnrollFailed()
        self.ts.markFinal("test_courseEnrollment", result,
                          "Enrollment Failed Verification")