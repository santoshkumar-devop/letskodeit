import pytest
from base.webdriverfactory import WebDriverFactory
from pages.home.login_page import LoginPage


@pytest.fixture(scope="class")
def oneTimeSetUp(request):
    print("Running one time setUp")
    browser_name = request.config.getoption("--browser_name")
    wdf = WebDriverFactory(browser_name=browser_name, headless=False)
    driver_instance = wdf.getWebDriverInstance()

    if request.cls is not None:
        request.cls.page = driver_instance

    yield
    wdf.close()
    print("Running one time tearDown")

@pytest.fixture()
def setUp(request):
    print("Running method level setUp")
    lp = LoginPage(request.cls.page)
    lp.login("test@email.com", "abcabc")
    yield
    print("Running method level tearDown")
    lp.logout()

def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chromium", help="Browser name: chromium, firefox, webkit")
    parser.addoption("--osType", help="Type of operating system")

@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser_name")