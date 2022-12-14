import allure
import pytest

from mysql.models.test_user_model import TestUserModel
from api.client import ApiClient
from static.credentials import CREDENTIALS
from utils.user_builder import *


class BaseApiTest:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, config, mysql_client):
        self.api_client: ApiClient = ApiClient(base_url='http://0.0.0.0:8080', username=CREDENTIALS['main']['username'],
                                               password=CREDENTIALS['main']['password'])
        if self.authorize:
            self.api_client.authorization(check_cookies=True)

        self.sql_client = mysql_client

    @pytest.fixture(scope='function')
    def clear_cookies(self):
        self.api_client.session.cookies.clear()

    @pytest.fixture(scope='function')
    def create_full_user(self):
        new_user = full_user()
        create_user_response = self.api_client.post_create_user(new_user=new_user)
        yield new_user, create_user_response

        self.api_client.delete_user(username=new_user['username'])

    @pytest.fixture(scope='function')
    def create_user_without_name(self):
        new_user = user_without_name()
        create_user_response = self.api_client.post_create_user(new_user=new_user)
        yield new_user, create_user_response

        self.api_client.delete_user(username=new_user['username'])

    @pytest.fixture(scope='function')
    def create_user_name_null_str(self):
        new_user = full_user(name_min_len=0)
        create_user_response = self.api_client.post_create_user(new_user=new_user)
        yield new_user, create_user_response

        self.api_client.delete_user(username=new_user['username'])

    @pytest.fixture(scope='function')
    def create_user_name_overfull_str(self):
        new_user = full_user(name_min_len=260)
        create_user_response = self.api_client.post_create_user(new_user=new_user)
        yield new_user, create_user_response

        self.api_client.delete_user(username=new_user['username'])

    @pytest.fixture(scope='function')
    def create_user_without_surname(self):
        new_user = user_without_surname()
        create_user_response = self.api_client.post_create_user(new_user=new_user)
        yield new_user, create_user_response

        self.api_client.delete_user(username=new_user['username'])

    @pytest.fixture(scope='function')
    def create_user_surname_null_str(self):
        new_user = full_user(surname_min_len=0)
        create_user_response = self.api_client.post_create_user(new_user=new_user)
        yield new_user, create_user_response

        self.api_client.delete_user(username=new_user['username'])

    @pytest.fixture(scope='function')
    def create_user_surname_overfull_str(self):
        new_user = full_user(surname_min_len=260)
        create_user_response = self.api_client.post_create_user(new_user=new_user)
        yield new_user, create_user_response

        self.api_client.delete_user(username=new_user['username'])

    @pytest.fixture(scope='function')
    def create_user_without_middle_name(self):
        new_user = user_without_middle_name()
        create_user_response = self.api_client.post_create_user(new_user=new_user)
        yield new_user, create_user_response

        self.api_client.delete_user(username=new_user['username'])

    @pytest.fixture(scope='function')
    def create_user_middle_name_null_str(self):
        new_user = full_user(middle_name_min_len=0)
        create_user_response = self.api_client.post_create_user(new_user=new_user)
        yield new_user, create_user_response

        self.api_client.delete_user(username=new_user['username'])

    @pytest.fixture(scope='function')
    def create_user_middle_name_overfull_str(self):
        new_user = full_user(middle_name_min_len=260)
        create_user_response = self.api_client.post_create_user(new_user=new_user)
        yield new_user, create_user_response

        self.api_client.delete_user(username=new_user['username'])

    @pytest.fixture(scope='function')
    def create_user_without_username(self):
        new_user = user_without_username()
        create_user_response = self.api_client.post_create_user(new_user=new_user)
        yield new_user, create_user_response

    @pytest.fixture(scope='function')
    def create_user_username_null_str(self):
        new_user = full_user(username_min_len=0)
        create_user_response = self.api_client.post_create_user(new_user=new_user)
        yield new_user, create_user_response

        self.api_client.delete_user(username=new_user['username'])

    @pytest.fixture(scope='function')
    def create_user_username_overfull_str(self):
        new_user = full_user(username_min_len=20)
        create_user_response = self.api_client.post_create_user(new_user=new_user)
        yield new_user, create_user_response

        self.api_client.delete_user(username=new_user['username'])

    @pytest.fixture(scope='function')
    def create_user_username_duplicate(self):
        first_user = full_user()
        create_first_user_response = self.api_client.post_create_user(new_user=first_user)
        second_user = full_user()
        second_user['username'] = first_user['username']
        create_second_user_response = self.api_client.post_create_user(new_user=second_user)
        yield second_user, create_second_user_response

        self.api_client.delete_user(username=first_user['username'])
        self.api_client.delete_user(username=second_user['username'])

    @pytest.fixture(scope='function')
    def create_user_without_email(self):
        new_user = user_without_email()
        create_user_response = self.api_client.post_create_user(new_user=new_user)
        yield new_user, create_user_response

        self.api_client.delete_user(username=new_user['username'])

    @pytest.fixture(scope='function')
    def create_user_email_null_str(self):
        new_user = full_user()
        new_user['email'] = ''
        create_user_response = self.api_client.post_create_user(new_user=new_user)
        yield new_user, create_user_response

        self.api_client.delete_user(username=new_user['username'])

    @pytest.fixture(scope='function')
    def create_user_email_overfull_str(self):
        new_user = full_user(email_min_len=70)
        create_user_response = self.api_client.post_create_user(new_user=new_user)
        yield new_user, create_user_response

        self.api_client.delete_user(username=new_user['username'])

    @pytest.fixture(scope='function')
    def create_user_email_wrong_mask(self):
        new_user = full_user()
        new_user['email'] = 'aaaaa'
        create_user_response = self.api_client.post_create_user(new_user=new_user)
        yield new_user, create_user_response

        self.api_client.delete_user(username=new_user['username'])

    @pytest.fixture(scope='function')
    def create_user_email_duplicate(self):
        first_user = full_user()
        create_first_user_response = self.api_client.post_create_user(new_user=first_user)
        second_user = full_user()
        second_user['email'] = first_user['email']
        create_second_user_response = self.api_client.post_create_user(new_user=second_user)
        yield second_user, create_second_user_response

        self.api_client.delete_user(username=first_user['username'])
        self.api_client.delete_user(username=second_user['username'])

    @pytest.fixture(scope='function')
    def create_user_without_password(self):
        new_user = user_without_password()
        create_user_response = self.api_client.post_create_user(new_user=new_user)
        yield new_user, create_user_response

        self.api_client.delete_user(username=new_user['username'])

    @pytest.fixture(scope='function')
    def create_user_password_null_str(self):
        new_user = full_user()
        new_user['password'] = ''
        create_user_response = self.api_client.post_create_user(new_user=new_user)
        yield new_user, create_user_response

        self.api_client.delete_user(username=new_user['username'])

    @pytest.fixture(scope='function')
    def create_user_password_overfull_str(self):
        new_user = full_user(password_len=260)
        create_user_response = self.api_client.post_create_user(new_user=new_user)
        yield new_user, create_user_response

        self.api_client.delete_user(username=new_user['username'])

    @pytest.fixture(scope='function')
    def delete_existing_user(self):
        new_user = full_user()
        create_user_response = self.api_client.post_create_user(new_user=new_user)
        delete_user_response = self.api_client.delete_user(username=new_user['username'])
        yield new_user, delete_user_response

    @pytest.fixture(scope='function')
    def delete_non_existing_user(self):
        new_user = full_user()
        db_data = self.sql_client.get_all_table_data(table_model=TestUserModel)
        delete_user_response = self.api_client.delete_user(username=new_user['username'])
        yield new_user, delete_user_response, len(db_data)

    @pytest.fixture(scope='function')
    def change_password_new(self):
        first_user = full_user()
        create_user_response = self.api_client.post_create_user(new_user=first_user)
        second_user = full_user()
        change_password_response = self.api_client.put_change_password(username=first_user['username'],
                                                                       new_password=second_user['password'])

        yield first_user, change_password_response, second_user['password']

        self.api_client.delete_user(username=first_user['username'])

    @pytest.fixture(scope='function')
    def change_password_old(self):
        first_user = full_user()
        create_user_response = self.api_client.post_create_user(new_user=first_user)
        change_password_response = self.api_client.put_change_password(username=first_user['username'],
                                                                       new_password=first_user['password'])

        yield first_user, change_password_response

        self.api_client.delete_user(username=first_user['username'])

    @pytest.fixture(scope='function')
    def change_password_non_existing_user(self):
        first_user = full_user()
        change_password_response = self.api_client.put_change_password(username=first_user['username'],
                                                                       new_password=first_user['password'])

        yield first_user, change_password_response

        self.api_client.delete_user(username=first_user['username'])

    @pytest.fixture(scope='function')
    def block_active_user(self):
        user = full_user()
        create_user_response = self.api_client.post_create_user(new_user=user)
        block_response = self.api_client.post_block_user(username=user['username'])

        yield user, block_response

        self.api_client.delete_user(username=user['username'])

    @pytest.fixture(scope='function')
    def block_blocked_user(self):
        user = full_user()
        create_user_response = self.api_client.post_create_user(new_user=user)
        block_response = self.api_client.post_block_user(username=user['username'])
        block_response_2 = self.api_client.post_block_user(username=user['username'])

        yield user, block_response_2

        self.api_client.delete_user(username=user['username'])

    @pytest.fixture(scope='function')
    def block_non_existing_user(self):
        user = full_user()
        block_response = self.api_client.post_block_user(username=user['username'])
        db = self.sql_client.get_all_table_data(table_model=TestUserModel)
        yield user, block_response, len(db)

    @pytest.fixture(scope='function')
    def unblock_blocked_user(self):
        user = full_user()
        create_user_response = self.api_client.post_create_user(new_user=user)
        block_response = self.api_client.post_block_user(username=user['username'])
        db = self.sql_client.get_table_data(table_model=TestUserModel, email=user['email'])
        unblock_response = self.api_client.post_accept_user(username=user['username'])

        yield user, unblock_response

        self.api_client.delete_user(username=user['username'])

    @pytest.fixture(scope='function')
    def unblock_active_user(self):
        user = full_user()
        create_user_response = self.api_client.post_create_user(new_user=user)
        unblock_response = self.api_client.post_accept_user(username=user['username'])

        yield user, unblock_response

        self.api_client.delete_user(username=user['username'])

    @pytest.fixture(scope='function')
    def unblock_non_existing_user(self):
        user = full_user()
        db = self.sql_client.get_all_table_data(table_model=TestUserModel)
        unblock_response = self.api_client.post_accept_user(username=user['username'])

        yield user, unblock_response, len(db)

        self.api_client.delete_user(username=user['username'])

