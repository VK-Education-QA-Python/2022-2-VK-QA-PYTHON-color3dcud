import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from ui.fixtures import *


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome")
    parser.addoption("--url", default='https://target-sandbox.my.com/')
    parser.addoption("--headless", action="store_true")


@pytest.fixture(scope='session')
def config(request):
    browser = request.config.getoption("--browser")
    url = request.config.getoption("--url")
    if request.config.getoption("--headless"):
        headless = True
    else:
        headless = False

    return {"browser": browser, "url": url, "headless": headless}


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture()
def files_path(repo_root):
    return os.path.join(repo_root, 'files', '')
