import os

import pytest

from api.client import ApiClient
from static.credentials import *


def pytest_addoption(parser):
    parser.addoption("--url", default='https://target-sandbox.my.com/')


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')

    return {'url': url}


@pytest.fixture(scope='session')
def api_client(config):
    return ApiClient(base_url=config['url'], login=LOGIN, password=PASSWORD)


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture()
def files_path(repo_root):
    return os.path.join(repo_root, 'files', '')
