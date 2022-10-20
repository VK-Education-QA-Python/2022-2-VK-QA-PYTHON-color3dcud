import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.new_campaign_page import NewCampaignPage
from ui.pages.segments_page import SegmentsPage
from ui.pages.new_segment_page import NewSegmentPage
from ui.pages.groups_page import GroupsPage

login = 'hsabuse@yandex.ru'
password = 'Qwe123-'


@pytest.fixture(scope='function')
def driver(config):
    browser = config["browser"]
    url = config["url"]
    headless = config["headless"]
    opt = Options()

    if headless:
        opt.add_argument('--headless')
        opt.add_argument('--disable-gpu')
    if browser == "chrome":
        driver = webdriver.Chrome(executable_path=ChromeDriverManager(version='105.0.5195.19').install(), options=opt)
    elif browser == "firefox":
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    else:
        raise RuntimeError(f'Unsupported browser: "{browser}"')

    driver.get(url)

    if headless:
        driver.set_window_size(1440, 900)
    else:
        driver.maximize_window()
    yield driver
    driver.quit()


def get_driver(config):
    browser = config["browser"]
    opt = Options()

    opt.add_argument('--headless')
    opt.add_argument('--disable-gpu')
    if browser == "chrome":
        driver = webdriver.Chrome(executable_path=ChromeDriverManager(version='105.0.5195.19').install(), options=opt)
    elif browser == "firefox":
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    else:
        raise RuntimeError(f'Unsupported browser: "{browser}"')

    return driver


@pytest.fixture(scope='session')
def cookies(config):
    driver = get_driver(config)
    login_page = MainPage(driver=driver, check_opened=False)
    login_page.driver.get(login_page.url)
    login_page.login(login=login, password=password)
    cookies = driver.get_cookies()
    driver.quit()
    return cookies


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def main_page(driver):
    return MainPage(driver=driver, check_opened=False)


@pytest.fixture
def dashboard_page(driver):
    return DashboardPage(driver=driver, check_opened=False)


@pytest.fixture
def new_campaign_page(driver):
    return NewCampaignPage(driver=driver, check_opened=False)


@pytest.fixture
def segments_page(driver):
    return SegmentsPage(driver=driver, check_opened=False)


@pytest.fixture
def new_segment_page(driver):
    return NewSegmentPage(driver=driver, check_opened=False)


@pytest.fixture
def groups_page(driver):
    return GroupsPage(driver=driver, check_opened=False)
