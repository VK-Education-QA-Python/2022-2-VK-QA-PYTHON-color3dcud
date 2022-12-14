import datetime
import logging
import os
import shutil

import allure

from mysql.client import MysqlClient
from static.credentials import DB_CREDENTIALS
from ui.fixtures import *



def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome')
    parser.addoption("--url", default=APP_CONFIG['APP_URL'])
    parser.addoption("--headless", action="store_true")
    parser.addoption('--debug_log', action='store_true')
    parser.addoption('--selenoid', action='store_true')
    parser.addoption('--vnc', action='store_true')


def pytest_configure(config):
    mysql_client = MysqlClient(user=DB_CREDENTIALS['user'], password=DB_CREDENTIALS['password'],
                               db_name=DB_CREDENTIALS['db_name'])
    mysql_client.connect(db_created=True)

    config.mysql_client = mysql_client


@pytest.fixture(scope='session')
def config(request):
    browser = request.config.getoption('--browser')
    url = request.config.getoption('--url')

    if request.config.getoption("--headless"):
        headless = True
    else:
        headless = False

    debug_log = request.config.getoption('--debug_log')

    if request.config.getoption('--selenoid'):
        if request.config.getoption('--vnc'):
            vnc = True
        else:
            vnc = False
        selenoid = APP_CONFIG['SELENOID_URL']
    else:
        selenoid = None
        vnc = False

    return {
        'browser': browser,
        'url': url,
        'headless': headless,
        'debug_log': debug_log,
        'selenoid': selenoid,
        'vnc': vnc
    }


@pytest.fixture(scope='session')
def mysql_client(request) -> MysqlClient:
    client = request.config.mysql_client
    yield client
    client.connection.close()


@pytest.fixture(scope='session')
def base_temp_dir():
    base_dir = f'/tmp/tests/{datetime.datetime.now()}'
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    return base_dir


@pytest.fixture(scope='function')
def temp_dir(request, base_temp_dir):
    test_dir = os.path.join(base_temp_dir, request._pyfuncitem.nodeid)
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='function')
def logger(temp_dir, config):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    log_file = os.path.join(temp_dir, 'test.log')
    log_level = logging.DEBUG if config['debug_log'] else logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()
