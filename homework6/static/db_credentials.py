import sys

USER = 'root'
DB_NAME = 'TEST_SQL'


def password():
    if sys.platform == 'darwin':
        password_value = '0000'
    else:
        password_value = 'pass'

    return password_value
