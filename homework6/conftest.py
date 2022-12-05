import os

import pytest

from mysql.client import MysqlClient
from static.db_credentials import *
from static.tables_base import TABLES_BASE


def pytest_configure(config):
    mysql_client = MysqlClient(user=USER, password=password(), db_name=DB_NAME)
    if not hasattr(config, 'workerinput'):
        mysql_client.create_db()
    mysql_client.connect(db_created=True)
    if not hasattr(config, 'workerinput'):
        for table in TABLES_BASE:
            table_name = table
            table_base = TABLES_BASE[table]
            mysql_client.create_table(table_name=table_name, table_base=table_base)

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
