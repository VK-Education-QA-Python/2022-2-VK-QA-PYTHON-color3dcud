import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from static.app_config import APP_CONFIG
from ui.pages.login_page import LoginPage
from ui.pages.main_page import MainPage
from ui.pages.registration_page import RegistrationPage


@pytest.fixture(scope='function')
def driver(config, temp_dir):
    browser = config['browser']
    url = config['url']
    headless = config["headless"]
    selenoid = config['selenoid']
    vnc = config['vnc']
    options = Options()

    if headless:
        options.add_argument('--headless')

    if selenoid:
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--headless')
        capabilities = {
            "browserName": "chrome",
            "browserVersion": "108.0",
            "selenoid:options": {
                "enableVideo": False
            }
        }
        if vnc:
            capabilities['enableVNC'] = True

        driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=options,
            desired_capabilities=capabilities
        )
    elif browser == 'chrome':
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    elif browser == 'firefox':
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


@pytest.fixture
def login_page(driver):
    return LoginPage(driver=driver)


@pytest.fixture
def registration_page(driver):
    return RegistrationPage(driver=driver)


@pytest.fixture
def main_page(driver):
    return MainPage(driver=driver)
