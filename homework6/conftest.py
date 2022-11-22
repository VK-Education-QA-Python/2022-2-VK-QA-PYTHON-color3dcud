import os
import pytest
from mysql.client import MysqlClient
from static.db_credentials import *


def pytest_configure(config):
    mysql_client = MysqlClient(user=USER, password=PASSWORD, db_name=DB_NAME)
    if not hasattr(config, 'workerinput'):
        mysql_client.create_db()
    mysql_client.connect(db_created=True)
    if not hasattr(config, 'workerinput'):
        mysql_client.create_table_total_requests()
        mysql_client.create_table_req_by_method()
        mysql_client.create_table_top_ten_requests()
        mysql_client.create_table_biggest_req()
        mysql_client.create_table_top_ips_500()

    config.mysql_client = mysql_client


@pytest.fixture(scope='session')
def mysql_client(request) -> MysqlClient:
    client = request.config.mysql_client
    yield client
    client.connection.close()


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='session')
def files_path(repo_root):
    return os.path.join(repo_root, 'utils', '')
