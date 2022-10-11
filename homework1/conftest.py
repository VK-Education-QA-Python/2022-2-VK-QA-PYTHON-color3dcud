import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")
    parser.addoption("--url", default="https://target-sandbox.my.com/")
    parser.addoption("--headless", action="store_true")


@pytest.fixture()
def config(request):
    browser = request.config.getoption("--browser")
    url = request.config.getoption("--url")
    if request.config.getoption("--headless"):
        headless = True
    else:
        headless = False

    return {"browser": browser, "url": url, "headless": headless}


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
