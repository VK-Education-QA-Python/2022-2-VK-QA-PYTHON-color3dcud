import time

import allure
import pytest

from mysql.models.test_user_model import TestUserModel
from tests.tests_api.base_api import BaseApiTest

from static.api.response_body import RESPONSE_BODY
from static.credentials import CREDENTIALS
from utils.random_credentials import random_creds


@allure.parent_suite('Тестирование API')
class TestApi:

    @allure.suite('Запросы от неавторизованного пользователя')
    class TestUnauthorizedApi(BaseApiTest):

        @allure.feature('Авторизация пользователя - POST /login')
        class TestAuthorization(BaseApiTest):
            authorize = False

            @allure.title('Авторизация с корректными данными')
            def test_login_correct(self, clear_cookies):
                clear_cookies
                response = self.api_client.authorization(username=CREDENTIALS['main']['username'],
                                                         password=CREDENTIALS['main']['password'],
                                                         check_cookies=False)

                expected_code = RESPONSE_BODY['auth_correct']['code']
                assert response.status_code == expected_code, f'Код ответа {response.status_code} != {expected_code}'

                cookies = self.api_client.session.cookies.get_dict()
                for i in range(len(self.api_client.AUTHORIZATION_COOKIES)):
                    assert self.api_client.AUTHORIZATION_COOKIES[i] in cookies, f'Авторизационные cookies не получены!'

                clear_cookies

            @allure.title('Авторизация с некорректными данными')
            def test_login_incorrect(self, clear_cookies):
                clear_cookies
                creds = random_creds()
                response = self.api_client.authorization(username=creds['username'],
                                                         password=creds['password'],
                                                         check_cookies=False)

                expected_code = RESPONSE_BODY['auth_incorrect']['code']
                assert response.status_code == expected_code, f'Код ответа {response.status_code} != {expected_code}'

                cookies = self.api_client.session.cookies.get_dict()
                for i in range(len(self.api_client.AUTHORIZATION_COOKIES)):
                    assert self.api_client.AUTHORIZATION_COOKIES[i] not in cookies, f'Авторизационные cookies не ' \
                                                                                    f'получены!'
                clear_cookies

            @allure.title('Авторизация с данными заблокированного пользователя')
            def test_login_blocked(self, clear_cookies):
                clear_cookies
                response = self.api_client.authorization(username=CREDENTIALS['blocked_user']['username'],
                                                         password=CREDENTIALS['blocked_user']['password'],
                                                         check_cookies=False)

                expected_code = RESPONSE_BODY['auth_blocked']['code']
                assert response.status_code == expected_code, f'Код ответа {response.status_code} != {expected_code}'

                cookies = self.api_client.session.cookies.get_dict()
                for i in range(len(self.api_client.AUTHORIZATION_COOKIES)):
                    assert self.api_client.AUTHORIZATION_COOKIES[i] not in cookies, f'Авторизационные cookies не ' \
                                                                                    f'получены!'
                clear_cookies

        @allure.feature('Ограничение запросов (кроме /login) для неавторизованного пользователя')
        class TestUnauthorizedEndpoints(BaseApiTest):
            authorize = False

            @allure.title('Создание пользователя без авторизации')
            def test_unauthorized_create_user(self, create_full_user, clear_cookies):
                clear_cookies
                new_user, response = create_full_user
                db_data = self.sql_client.get_table_data(table_model=TestUserModel, email=new_user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data is None, f'В базу данных был записан пользователь!'

                with allure.step('Проверка тела запроса'):
                    expected_body = RESPONSE_BODY['create_full_user_unauthorized']['body']
                    actual_body = response.json()
                    assert actual_body.get('detail', None) == expected_body['detail'], f'Поле detail = ' \
                                                                                       f'{actual_body.get("detail", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["detail"]}'
                    assert actual_body.get('status', None) == expected_body['status'], f'Поле status = ' \
                                                                                       f'{actual_body.get("status", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["status"]}'
                    assert actual_body.get('url', None) == expected_body['url'], f'Поле url = ' \
                                                                                 f'{actual_body.get("url", None)} !=' \
                                                                                 f'{expected_body["url"]}'

                with allure.step('Проверка кода ответа'):
                    expected_code = RESPONSE_BODY['create_full_user_unauthorized']['code']
                    actual_code = response.status_code
                    assert actual_code == expected_code, f'Код ответа {actual_code} != {expected_code}'

            @allure.title('Удаление пользователя без авторизации')
            def test_unauthorized_delete_user(self, clear_cookies):
                clear_cookies
                db_data_before = self.sql_client.get_all_table_data(table_model=TestUserModel)
                response = self.api_client.delete_user(username='delete_user')
                db_data_after = self.sql_client.get_all_table_data(table_model=TestUserModel)

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data_after == db_data_before, f'Данные в БД изменились!'

                with allure.step('Проверка тела запроса'):
                    expected_body = RESPONSE_BODY['delete_user_unauthorized']['body']
                    actual_body = response.json()
                    assert actual_body.get('detail', None) == expected_body['detail'], f'Поле detail = ' \
                                                                                       f'{actual_body.get("detail", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["detail"]}'
                    assert actual_body.get('status', None) == expected_body['status'], f'Поле status = ' \
                                                                                       f'{actual_body.get("status", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["status"]}'
                    assert actual_body.get('url', None) == expected_body['url'], f'Поле url = ' \
                                                                                 f'{actual_body.get("url", None)} !=' \
                                                                                 f'{expected_body["url"]}'

                with allure.step('Проверка кода ответа'):
                    expected_code = RESPONSE_BODY['delete_user_unauthorized']['code']
                    actual_code = response.status_code
                    assert actual_code == expected_code, f'Код ответа {actual_code} != {expected_code}'

            @allure.title('Изменение пароля пользователя без авторизации')
            def test_unauthorized_change_user_pass(self, clear_cookies):
                clear_cookies
                username = 'test_user'
                db_data_before = self.sql_client.get_all_table_data(table_model=TestUserModel)
                response = self.api_client.put_change_password(username=username, new_password='test_test')
                db_data_after = self.sql_client.get_all_table_data(table_model=TestUserModel)

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data_after == db_data_before, f'Данные в БД изменились!'

                with allure.step('Проверка тела запроса'):
                    expected_body = RESPONSE_BODY['change_pass_unauthorized']['body']
                    actual_body = response.json()
                    assert actual_body.get('detail', None) == expected_body['detail'], f'Поле detail = ' \
                                                                                       f'{actual_body.get("detail", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["detail"]}'
                    assert actual_body.get('status', None) == expected_body['status'], f'Поле status = ' \
                                                                                       f'{actual_body.get("status", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["status"]}'
                    assert actual_body.get('url', None) == expected_body['url'], f'Поле url = ' \
                                                                                 f'{actual_body.get("url", None)} !=' \
                                                                                 f'{expected_body["url"]}'

                with allure.step('Проверка кода ответа'):
                    expected_code = RESPONSE_BODY['change_pass_unauthorized']['code']
                    actual_code = response.status_code
                    assert actual_code == expected_code, f'Код ответа {actual_code} != {expected_code}'

            @allure.title('Блокировка пользователя без авторизации')
            def test_unauthorized_block_user(self, clear_cookies):
                clear_cookies
                username = 'test_user'
                db_data_before = self.sql_client.get_all_table_data(table_model=TestUserModel)
                response = self.api_client.post_block_user(username=username)
                db_data_after = self.sql_client.get_all_table_data(table_model=TestUserModel)

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data_after == db_data_before, f'Данные в БД изменились!'

                with allure.step('Проверка тела запроса'):
                    expected_body = RESPONSE_BODY['block_unauthorized']['body']
                    actual_body = response.json()
                    assert actual_body.get('detail', None) == expected_body['detail'], f'Поле detail = ' \
                                                                                       f'{actual_body.get("detail", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["detail"]}'
                    assert actual_body.get('status', None) == expected_body['status'], f'Поле status = ' \
                                                                                       f'{actual_body.get("status", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["status"]}'
                    assert actual_body.get('url', None) == expected_body['url'], f'Поле url = ' \
                                                                                 f'{actual_body.get("url", None)} !=' \
                                                                                 f'{expected_body["url"]}'

                with allure.step('Проверка кода ответа'):
                    expected_code = RESPONSE_BODY['block_unauthorized']['code']
                    actual_code = response.status_code
                    assert actual_code == expected_code, f'Код ответа {actual_code} != {expected_code}'

            @allure.title('Разблокировка пользователя без авторизации')
            def test_unauthorized_unblock_user(self, clear_cookies):
                clear_cookies
                username = 'test_user'
                db_data_before = self.sql_client.get_all_table_data(table_model=TestUserModel)
                response = self.api_client.post_accept_user(username=username)
                db_data_after = self.sql_client.get_all_table_data(table_model=TestUserModel)

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data_after == db_data_before, f'Данные в БД изменились!'

                with allure.step('Проверка тела запроса'):
                    expected_body = RESPONSE_BODY['unblock_unauthorized']['body']
                    actual_body = response.json()
                    assert actual_body.get('detail', None) == expected_body['detail'], f'Поле detail = ' \
                                                                                       f'{actual_body.get("detail", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["detail"]}'
                    assert actual_body.get('status', None) == expected_body['status'], f'Поле status = ' \
                                                                                       f'{actual_body.get("status", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["status"]}'
                    assert actual_body.get('url', None) == expected_body['url'], f'Поле url = ' \
                                                                                 f'{actual_body.get("url", None)} !=' \
                                                                                 f'{expected_body["url"]}'

                with allure.step('Проверка кода ответа'):
                    expected_code = RESPONSE_BODY['unblock_unauthorized']['code']
                    actual_code = response.status_code
                    assert actual_code == expected_code, f'Код ответа {actual_code} != {expected_code}'

    @allure.suite('Запросы от авторизованных пользователей')
    class TestAuthorizedApi(BaseApiTest):

        @allure.feature('Создание пользователя - POST /api/user')
        class TestUserAdd(BaseApiTest):

            @allure.title('ТУТ БАГ! - КОД ОВТЕТВ. Создание пользователя с заполнением всех полей')
            @pytest.mark.API
            def test_create_full_user(self, create_full_user):
                new_user, response = create_full_user
                db_data = self.sql_client.get_table_data(table_model=TestUserModel, email=new_user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data.name == new_user['name'], f'Имена не совпадают! Подробности в отчете'
                    assert db_data.surname == new_user['surname'], f'Фамилии не совпадают! Подробности в отчете'
                    assert db_data.middle_name == new_user['middle_name'], f'Отчества не совпадают! Подробности в отчете'
                    assert db_data.username == new_user['username'], f'Юзернеймы не совпадают! Подробности в отчете'
                    assert db_data.password == new_user['password'], f'Пароли не совпадают! Подробности в отчете'
                    assert db_data.email == new_user['email'], f'Почты не совпадают! Подробности в отчете'

                with allure.step('Проверка тела запроса'):
                    expected_body = RESPONSE_BODY['create_full_user']['body']
                    actual_body = response.json()
                    assert actual_body.get('detail', None) == expected_body['detail'], f'Поле detail = ' \
                                                                                       f'{actual_body.get("detail", None)}'\
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["detail"]}'
                    assert actual_body.get('status', None) == expected_body['status'], f'Поле status = ' \
                                                                                       f'{actual_body.get("status", None)}'\
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["status"]}'

                with allure.step('Проверка кода ответа'):
                    expected_code = RESPONSE_BODY['create_full_user']['code']
                    assert response.status_code == expected_code, f'Код ответа {response.status_code} != {expected_code}'

            @allure.title('ТУТ БАГ! - КОД ОВТЕТВ. Создание пользователя без имени')
            @pytest.mark.API
            def test_create_user_without_name(self, create_user_without_name):
                new_user, response = create_user_without_name
                db_data = self.sql_client.get_table_data(table_model=TestUserModel, email=new_user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data is None, f'В базу данных был записан пользователь!'

                with allure.step('Проверка тела запроса'):
                    expected_body = RESPONSE_BODY['create_user_without_name']['body']
                    actual_body = response.json()
                    assert actual_body.get('detail', None) == expected_body['detail'], f'Поле detail = ' \
                                                                                       f'{actual_body.get("detail", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["detail"]}'
                    assert actual_body.get('status', None) == expected_body['status'], f'Поле status = ' \
                                                                                       f'{actual_body.get("status", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["status"]}'

                with allure.step('Проверка кода ответа'):
                    expected_code = RESPONSE_BODY['create_user_without_name']['code']
                    assert response.status_code == expected_code, f'Код ответа {response.status_code} != {expected_code}'

            @allure.title('Создание пользователя без фамилии')
            @pytest.mark.API
            def test_create_user_without_surname(self, create_user_without_surname):
                new_user, response = create_user_without_surname
                db_data = self.sql_client.get_table_data(table_model=TestUserModel, email=new_user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data is None, f'В базу данных был записан пользователь!'

                with allure.step('Проверка тела запроса'):
                    expected_body = RESPONSE_BODY['create_user_without_surname']['body']
                    actual_body = response.json()
                    assert actual_body.get('detail', None) == expected_body['detail'], f'Поле detail = ' \
                                                                                       f'{actual_body.get("detail", None)}'\
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["detail"]}'
                    assert actual_body.get('status', None) == expected_body['status'], f'Поле status = ' \
                                                                                       f'{actual_body.get("status", None)}'\
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["status"]}'

                with allure.step('Проверка кода ответа'):
                    expected_code = RESPONSE_BODY['create_user_without_surname']['code']
                    assert response.status_code == expected_code, f'Код ответа {response.status_code} != {expected_code}'

            @allure.title('Создание пользователя без отчества')
            @pytest.mark.API
            def test_create_user_without_middle_name(self, create_user_without_middle_name):
                new_user, response = create_user_without_middle_name
                db_data = self.sql_client.get_table_data(table_model=TestUserModel, email=new_user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data.name == new_user['name'], f'Имена не совпадают! Подробности в отчете'
                    assert db_data.surname == new_user['surname'], f'Фамилии не совпадают! Подробности в отчете'
                    assert db_data.middle_name is None, f'В БД записано отчество, но его не передавали!'
                    assert db_data.username == new_user['username'], f'Юзернеймы не совпадают! Подробности в отчете'
                    assert db_data.password == new_user['password'], f'Пароли не совпадают! Подробности в отчете'
                    assert db_data.email == new_user['email'], f'Почты не совпадают! Подробности в отчете'

                with allure.step('Проверка тела запроса'):
                    expected_body = RESPONSE_BODY['create_user_without_middle_name']['body']
                    actual_body = response.json()
                    assert actual_body.get('detail', None) == expected_body['detail'], f'Поле detail = ' \
                                                                                       f'{actual_body.get("detail", None)}'\
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["detail"]}'
                    assert actual_body.get('status', None) == expected_body['status'], f'Поле status = ' \
                                                                                       f'{actual_body.get("status", None)}'\
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["status"]}'

                with allure.step('Проверка кода ответа'):
                    expected_code = RESPONSE_BODY['create_user_without_middle_name']['code']
                    assert response.status_code == expected_code, f'Код ответа {response.status_code} != {expected_code}'

            @allure.title('Создание пользователя без имени пользователя')
            @pytest.mark.API
            def test_create_user_without_username(self, create_user_without_username):
                new_user, response = create_user_without_username
                db_data = self.sql_client.get_table_data(table_model=TestUserModel, email=new_user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data is None, f'В базу данных был записан пользователь!'

                with allure.step('Проверка тела запроса'):
                    expected_body = RESPONSE_BODY['create_user_without_username']['body']
                    actual_body = response.json()
                    assert actual_body.get('detail', None) == expected_body['detail'], f'Поле detail = ' \
                                                                                       f'{actual_body.get("detail", None)}'\
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["detail"]}'
                    assert actual_body.get('status', None) == expected_body['status'], f'Поле status = ' \
                                                                                       f'{actual_body.get("status", None)}'\
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["status"]}'

                with allure.step('Проверка кода ответа'):
                    expected_code = RESPONSE_BODY['create_user_without_username']['code']
                    assert response.status_code == expected_code, f'Код ответа {response.status_code} != {expected_code}'

            @allure.title('Создание пользователя без почты')
            @pytest.mark.API
            def test_create_user_without_email(self, create_user_without_email):
                new_user, response = create_user_without_email
                db_data = self.sql_client.get_table_data(table_model=TestUserModel, email=new_user['username'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data is None, f'В базу данных был записан пользователь!'

                with allure.step('Проверка тела запроса'):
                    expected_body = RESPONSE_BODY['create_user_without_email']['body']
                    actual_body = response.json()
                    assert actual_body.get('detail', None) == expected_body['detail'], f'Поле detail = ' \
                                                                                       f'{actual_body.get("detail", None)}'\
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["detail"]}'
                    assert actual_body.get('status', None) == expected_body['status'], f'Поле status = ' \
                                                                                       f'{actual_body.get("status", None)}'\
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["status"]}'

                with allure.step('Проверка кода ответа'):
                    expected_code = RESPONSE_BODY['create_user_without_email']['code']
                    assert response.status_code == expected_code, f'Код ответа {response.status_code} != {expected_code}'

            @allure.title('Создание пользователя без пароля')
            @pytest.mark.API
            def test_create_user_without_password(self, create_user_without_password):
                new_user, response = create_user_without_password
                db_data = self.sql_client.get_table_data(table_model=TestUserModel, email=new_user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data is None, f'В базу данных был записан пользователь!'

                with allure.step('Проверка тела запроса'):
                    expected_body = RESPONSE_BODY['create_user_without_password']['body']
                    actual_body = response.json()
                    assert actual_body.get('detail', None) == expected_body['detail'], f'Поле detail = ' \
                                                                                       f'{actual_body.get("detail", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["detail"]}'
                    assert actual_body.get('status', None) == expected_body['status'], f'Поле status = ' \
                                                                                       f'{actual_body.get("status", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["status"]}'

                with allure.step('Проверка кода ответа'):
                    expected_code = RESPONSE_BODY['create_user_without_password']['code']
                    assert response.status_code == expected_code, f'Код ответа {response.status_code} != {expected_code}'

            @allure.feature('Валидация полей регистрации - API')
            @pytest.mark.API
            class TestUserAddValidations(BaseApiTest):

                @allure.title('ТУТ БАГ! - ЗАПИСЫВАЕТСЯ ПОЛЬЗОВАТЕЛЬ В БД. Проверка валидации длины name - пустая строка')
                def test_name_len_zero(self, create_user_name_null_str):
                    new_user, response = create_user_name_null_str
                    db_data = self.sql_client.get_table_data(table_model=TestUserModel, email=new_user['email'])

                    with allure.step('Проверка записанных в БД данных'):
                        assert db_data is None, f'В базу данных был записан пользователь!'

                    with allure.step('Проверка кода ответа'):
                        expected_code = RESPONSE_BODY['name_len_zero']['code']
                        assert response.status_code == expected_code, f'Код ответа {response.status_code} != {expected_code}'

                @allure.title('ТУТ БАГ! - Код ответа 500. Проверка валидации длины name - строка > 255 символов')
                def test_name_len_overfull(self, create_user_name_overfull_str):
                    new_user, response = create_user_name_overfull_str
                    db_data = self.sql_client.get_table_data(table_model=TestUserModel, email=new_user['email'])

                    with allure.step('Проверка записанных в БД данных'):
                        assert db_data is None, f'В базу данных был записан пользователь!'

                    with allure.step('Проверка кода ответа'):
                        expected_code = RESPONSE_BODY['name_len_overfull']['code']
                        assert response.status_code == expected_code, f'Код ответа {response.status_code} != {expected_code}'

                @allure.title('ТУТ БАГ! - ЗАПИСЫВАЕТСЯ ПОЛЬЗОВАТЕЛЬ В БД. Проверка валидации длины surnamename - пустая строка')
                def test_surname_len_zero(self, create_user_surname_null_str):
                    new_user, response = create_user_surname_null_str
                    db_data = self.sql_client.get_table_data(table_model=TestUserModel, email=new_user['email'])

                    with allure.step('Проверка записанных в БД данных'):
                        assert db_data is None, f'В базу данных был записан пользователь!'

                    with allure.step('Проверка кода ответа'):
                        expected_code = RESPONSE_BODY['surname_len_zero']['code']
                        assert response.status_code == expected_code, f'Код ответа {response.status_code} != {expected_code}'

                @allure.title('ТУТ БАГ! - Код ответа 500.Проверка валидации длины surname - строка > 255 символов')
                def test_surname_len_overfull(self, create_user_surname_overfull_str):
                    new_user, response = create_user_surname_overfull_str
                    db_data = self.sql_client.get_table_data(table_model=TestUserModel, email=new_user['email'])

                    with allure.step('Проверка записанных в БД данных'):
                        assert db_data is None, f'В базу данных был записан пользователь!'

                    with allure.step('Проверка кода ответа'):
                        expected_code = RESPONSE_BODY['surname_len_overfull']['code']
                        assert response.status_code == expected_code, f'Код ответа {response.status_code} != {expected_code}'

                @allure.title('ТУТ БАГ! - ЗАПИСЫВАЕТСЯ ПОЛЬЗОВАТЕЛЬ В БД. Проверка валидации длины middle_name - пустая строка')
                def test_middle_name_len_zero(self, create_user_middle_name_null_str):
                    new_user, response = create_user_middle_name_null_str
                    db_data = self.sql_client.get_table_data(table_model=TestUserModel, email=new_user['email'])

                    with allure.step('Проверка записанных в БД данных'):
                        assert db_data is None, f'В базу данных был записан пользователь!'

                    with allure.step('Проверка кода ответа'):
                        expected_code = RESPONSE_BODY['middle_name_len_zero']['code']
                        assert response.status_code == expected_code, f'Код ответа {response.status_code} != {expected_code}'

                @allure.title('ТУТ БАГ! - Код ответа 500.Проверка валидации длины middle_name - строка > 255 символов')
                def test_middle_name_len_overfull(self, create_user_middle_name_overfull_str):
                    new_user, response = create_user_middle_name_overfull_str
                    db_data = self.sql_client.get_table_data(table_model=TestUserModel, email=new_user['email'])

                    with allure.step('Проверка записанных в БД данных'):
                        assert db_data is None, f'В базу данных был записан пользователь!'

                    with allure.step('Проверка кода ответа'):
                        expected_code = RESPONSE_BODY['middle_name_len_overfull']['code']
                        assert response.status_code == expected_code, f'Код ответа {response.status_code} != {expected_code}'

                @allure.title('ТУТ БАГ! - ЗАПИСЫВАЕТСЯ ПОЛЬЗОВАТЕЛЬ В БД. Проверка валидации длины username - пустая строка')
                def test_username_len_zero(self, create_user_username_null_str):
                    new_user, response = create_user_username_null_str
                    db_data = self.sql_client.get_table_data(table_model=TestUserModel, email=new_user['email'])

                    with allure.step('Проверка записанных в БД данных'):
                        assert db_data is None, f'В базу данных был записан пользователь!'

                    with allure.step('Проверка кода ответа'):
                        expected_code = RESPONSE_BODY['username_len_zero']['code']
                        assert response.status_code == expected_code, f'Код ответа {response.status_code} != {expected_code}'

                @allure.title('ТУТ БАГ! - Код ответа 500.Проверка валидации длины username - строка > 16 символов')
                def test_username_len_overfull(self, create_user_username_overfull_str):
                    new_user, response = create_user_username_overfull_str
                    db_data = self.sql_client.get_table_data(table_model=TestUserModel, email=new_user['email'])

                    with allure.step('Проверка записанных в БД данных'):
                        assert db_data is None, f'В базу данных был записан пользователь!'

                    with allure.step('Проверка кода ответа'):
                        expected_code = RESPONSE_BODY['username_len_overfull']['code']
                        assert response.status_code == expected_code, f'Код ответа {response.status_code} != {expected_code}'

                @allure.title('ТУТ БАГ! - ЗАПИСЫВАЕТСЯ ПОЛЬЗОВАТЕЛЬ В БД. Проверка валидации длины email - пустая строка')
                def test_email_len_zero(self, create_user_email_null_str):
                    new_user, response = create_user_email_null_str
                    db_data = self.sql_client.get_table_data(table_model=TestUserModel, email=new_user['email'])

                    with allure.step('Проверка записанных в БД данных'):
                        assert db_data is None, f'В базу данных был записан пользователь!'

                    with allure.step('Проверка кода ответа'):
                        expected_code = RESPONSE_BODY['email_len_zero']['code']
                        assert response.status_code == expected_code, f'Код ответа {response.status_code} != {expected_code}'

                @allure.title('ТУТ БАГ! - Код ответа 500.Проверка валидации длины email - строка > 64 символов')
                def test_email_len_overfull(self, create_user_email_overfull_str):
                    new_user, response = create_user_email_overfull_str
                    db_data = self.sql_client.get_table_data(table_model=TestUserModel, email=new_user['email'])

                    with allure.step('Проверка записанных в БД данных'):
                        assert db_data is None, f'В базу данных был записан пользователь!'

                    with allure.step('Проверка кода ответа'):
                        expected_code = RESPONSE_BODY['email_len_overfull']['code']
                        assert response.status_code == expected_code, f'Код ответа {response.status_code} != {expected_code}'

                @allure.title('ТУТ БАГ! - НЕТ ВАЛИДАЦИИ ПО МАСКЕ.Проверка валидации маски email')
                def test_email_wrong_mask(self, create_user_email_wrong_mask):
                    new_user, response = create_user_email_wrong_mask
                    db_data = self.sql_client.get_table_data(table_model=TestUserModel, email=new_user['email'])

                    with allure.step('Проверка записанных в БД данных'):
                        assert db_data is None, f'В базу данных был записан пользователь!'

                    with allure.step('Проверка кода ответа'):
                        expected_code = RESPONSE_BODY['email_wrong_mask']['code']
                        assert response.status_code == expected_code, f'Код ответа {response.status_code} != {expected_code}'

                @allure.title('ТУТ БАГ! - ЗАПИСЫВАЕТСЯ ПОЛЬЗОВАТЕЛЬ В БД. Проверка валидации длины password - пустая строка')
                def test_password_len_zero(self, create_user_password_null_str):
                    new_user, response = create_user_password_null_str
                    db_data = self.sql_client.get_table_data(table_model=TestUserModel, email=new_user['email'])

                    with allure.step('Проверка записанных в БД данных'):
                        assert db_data is None, f'В базу данных был записан пользователь!'

                    with allure.step('Проверка кода ответа'):
                        expected_code = RESPONSE_BODY['password_len_zero']['code']
                        assert response.status_code == expected_code, f'Код ответа {response.status_code} != {expected_code}'

                @allure.title('ТУТ БАГ! - Код ответа 500.Проверка валидации длины password - строка > 255 символов')
                def test_password_len_overfull(self, create_user_password_overfull_str):
                    new_user, response = create_user_password_overfull_str
                    db_data = self.sql_client.get_table_data(table_model=TestUserModel, email=new_user['email'])

                    with allure.step('Проверка записанных в БД данных'):
                        assert db_data is None, f'В базу данных был записан пользователь!'

                    with allure.step('Проверка кода ответа'):
                        expected_code = RESPONSE_BODY['password_len_overfull']['code']
                        assert response.status_code == expected_code, f'Код ответа {response.status_code} != {expected_code}'

            @allure.feature('Добавление пользователей с НЕ уникальными полями')
            @pytest.mark.API
            class TestRepeatedFields(BaseApiTest):

                @allure.title('ТУТ БАГ! Сообщение не то! Повторяющийся email')
                def test_repeated_email(self, create_user_email_duplicate):
                    repeated_mail_user, response = create_user_email_duplicate

                    db_data = self.sql_client.get_table_data(table_model=TestUserModel,
                                                             username=repeated_mail_user['username'])

                    with allure.step('Проверка записанных в БД данных'):
                        assert db_data is None, f'В базу данных был записан пользователь!'

                    with allure.step('Проверка тела запроса'):
                        expected_body = RESPONSE_BODY['email_repeated']['body']
                        actual_body = response.json()
                        assert actual_body.get('detail', None) == expected_body['detail'], f'Поле detail = ' \
                                                                                           f'{actual_body.get("detail", None)}' \
                                                                                           f'не совпадает с ожидаемым - ' \
                                                                                           f'{expected_body["detail"]}'
                        assert actual_body.get('status', None) == expected_body['status'], f'Поле status = ' \
                                                                                           f'{actual_body.get("status", None)}' \
                                                                                           f'не совпадает с ожидаемым - ' \
                                                                                           f'{expected_body["status"]}'

                    with allure.step('Проверка кода ответа'):
                        expected_code = RESPONSE_BODY['email_repeated']['code']
                        assert response.status_code == expected_code, f'Код ответа {response.status_code} != {expected_code}'

                @allure.title('Повторяющийся username')
                def test_repeated_username(self, create_user_username_duplicate):
                    repeated_username_user, response = create_user_username_duplicate

                    db_data = self.sql_client.get_table_data(table_model=TestUserModel,
                                                             email=repeated_username_user['email'])

                    with allure.step('Проверка записанных в БД данных'):
                        assert db_data is None, f'В базу данных был записан пользователь!'

                    with allure.step('Проверка тела запроса'):
                        expected_body = RESPONSE_BODY['username_repeated']['body']
                        actual_body = response.json()
                        assert actual_body.get('detail', None) == expected_body['detail'], f'Поле detail = ' \
                                                                                           f'{actual_body.get("detail", None)}' \
                                                                                           f'не совпадает с ожидаемым - ' \
                                                                                           f'{expected_body["detail"]}'
                        assert actual_body.get('status', None) == expected_body['status'], f'Поле status = ' \
                                                                                           f'{actual_body.get("status", None)}' \
                                                                                           f'не совпадает с ожидаемым - ' \
                                                                                           f'{expected_body["status"]}'

                    with allure.step('Проверка кода ответа'):
                        expected_code = RESPONSE_BODY['username_repeated']['code']
                        assert response.status_code == expected_code, f'Код ответа {response.status_code} != {expected_code}'

        @allure.feature('Удаление пользователя - DELETE /api/user/<username>')
        class TestDeleteUser(BaseApiTest):

            @allure.title('Удаление существующего пользователя')
            @pytest.mark.API
            def test_delete_existing_user(self, delete_existing_user):
                user, response = delete_existing_user
                db_data = self.sql_client.get_table_data(table_model=TestUserModel, email=user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data is None, f'Пользователь не был удален из БД!'

                with allure.step('Проверка кода ответа'):
                    expected_code = RESPONSE_BODY['delete_existing_user']['code']
                    assert response.status_code == expected_code, f'Код ответа {response.status_code}!= {expected_code}'

            @allure.title('Удаление несуществующего пользователя')
            @pytest.mark.API
            def test_delete_no_existing_user(self, delete_non_existing_user):
                user, response, old_db_data = delete_non_existing_user
                db_data = self.sql_client.get_all_table_data(table_model=TestUserModel)

                with allure.step('Проверка записанных в БД данных'):
                    assert len(db_data) == len(db_data), f'Был удален существующий пользователь!'

                with allure.step('Проверка тела запроса'):
                    expected_body = RESPONSE_BODY['delete_non_existing_user']['body']
                    actual_body = response.json()
                    assert actual_body.get('detail', None) == expected_body['detail'], f'Поле detail = ' \
                                                                                       f'{actual_body.get("detail", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["detail"]}'
                    assert actual_body.get('status', None) == expected_body['status'], f'Поле status = ' \
                                                                                       f'{actual_body.get("status", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["status"]}'

                with allure.step('Проверка кода ответа'):
                    expected_code = RESPONSE_BODY['delete_non_existing_user']['code']
                    assert response.status_code == expected_code, f'Код ответа {response.status_code}!= {expected_code}'

        @allure.feature('Смена пароля - POST api/user/<username>/change-password')
        class TestChangePassword(BaseApiTest):

            @allure.title('Смена пароля на новый')
            @pytest.mark.API
            def test_change_password_new(self, change_password_new):
                user, response, new_pass = change_password_new

                db_data = self.sql_client.get_table_data(table_model=TestUserModel,
                                                         email=user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data.name == user['name'], f'Имена не совпадают! Подробности в отчете'
                    assert db_data.surname == user['surname'], f'Фамилии не совпадают! Подробности в отчете'
                    assert db_data.middle_name == user['middle_name'], f'Отчества не совпадают! Подробности в отчете'
                    assert db_data.username == user['username'], f'Юзернеймы не совпадают! Подробности в отчете'
                    assert db_data.password == new_pass, f'Пароли не совпадают! Подробности в отчете'
                    assert db_data.email == user['email'], f'Почты не совпадают! Подробности в отчете'

                with allure.step('Проверка кода ответа'):
                    expected_code = RESPONSE_BODY['change_pass_new']['code']
                    assert response.status_code == expected_code, f'Код ответа {response.status_code}!= {expected_code}'

            @allure.title('Смена пароля на тот же пароль')
            @pytest.mark.API
            def test_change_password_old(self, change_password_old):
                user, response = change_password_old

                db_data = self.sql_client.get_table_data(table_model=TestUserModel,
                                                         email=user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data.password == user['password'], f'Пароль изменился!'

                with allure.step('Проверка тела запроса'):
                    expected_body = RESPONSE_BODY['change_pass_old']['body']
                    actual_body = response.json()
                    assert actual_body.get('detail', None) == expected_body['detail'], f'Поле detail = ' \
                                                                                       f'{actual_body.get("detail", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["detail"]}'
                    assert actual_body.get('status', None) == expected_body['status'], f'Поле status = ' \
                                                                                       f'{actual_body.get("status", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["status"]}'

                with allure.step('Проверка кода ответа'):
                    expected_code = RESPONSE_BODY['change_pass_old']['code']
                    assert response.status_code == expected_code, f'Код ответа {response.status_code}!= {expected_code}'

            @allure.title('Смена пароля у несуществующего юзера')
            @pytest.mark.API
            def test_change_password_non_existing_user(self, change_password_non_existing_user):
                user, response = change_password_non_existing_user

                with allure.step('Проверка тела запроса'):
                    expected_body = RESPONSE_BODY['change_pass_non_existing_user']['body']
                    actual_body = response.json()
                    assert actual_body.get('detail', None) == expected_body['detail'], f'Поле detail = ' \
                                                                                       f'{actual_body.get("detail", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["detail"]}'
                    assert actual_body.get('status', None) == expected_body['status'], f'Поле status = ' \
                                                                                       f'{actual_body.get("status", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["status"]}'

                with allure.step('Проверка кода ответа'):
                    expected_code = RESPONSE_BODY['change_pass_non_existing_user']['code']
                    assert response.status_code == expected_code, f'Код ответа {response.status_code}!= {expected_code}'

        @allure.feature('Блокировка пользователя - POST /api/user/<username>/block')
        class TestBlockUser(BaseApiTest):

            @allure.title('Блокировка пользователя')
            @pytest.mark.API
            def test_block_unblocked_user(self, block_active_user):
                user, response = block_active_user

                db_data = self.sql_client.get_table_data(table_model=TestUserModel,
                                                         email=user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data.name == user['name'], f'Имена не совпадают! Подробности в отчете'
                    assert db_data.surname == user['surname'], f'Фамилии не совпадают! Подробности в отчете'
                    assert db_data.middle_name == user['middle_name'], f'Отчества не совпадают! Подробности в отчете'
                    assert db_data.username == user['username'], f'Юзернеймы не совпадают! Подробности в отчете'
                    assert db_data.password == user['password'], f'Пароли не совпадают! Подробности в отчете'
                    assert db_data.email == user['email'], f'Почты не совпадают! Подробности в отчете'
                    assert db_data.access == 0

                with allure.step('Проверка тела запроса'):
                    expected_body = RESPONSE_BODY['block_active_user']['body']
                    actual_body = response.json()
                    assert actual_body.get('detail', None) == expected_body['detail'], f'Поле detail = ' \
                                                                                       f'{actual_body.get("detail", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["detail"]}'
                    assert actual_body.get('status', None) == expected_body['status'], f'Поле status = ' \
                                                                                       f'{actual_body.get("status", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["status"]}'

                with allure.step('Проверка кода ответа'):
                    expected_code = RESPONSE_BODY['block_active_user']['code']
                    assert response.status_code == expected_code, f'Код ответа {response.status_code}!= {expected_code}'

            @allure.title('Блокировка заблокированного пользователя')
            @pytest.mark.API
            def test_block_blocked_user(self, block_blocked_user):
                user, response = block_blocked_user

                db_data = self.sql_client.get_table_data(table_model=TestUserModel,
                                                         email=user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data.name == user['name'], f'Имена не совпадают! Подробности в отчете'
                    assert db_data.surname == user['surname'], f'Фамилии не совпадают! Подробности в отчете'
                    assert db_data.middle_name == user['middle_name'], f'Отчества не совпадают! Подробности в отчете'
                    assert db_data.username == user['username'], f'Юзернеймы не совпадают! Подробности в отчете'
                    assert db_data.password == user['password'], f'Пароли не совпадают! Подробности в отчете'
                    assert db_data.email == user['email'], f'Почты не совпадают! Подробности в отчете'
                    assert db_data.access == 0

                with allure.step('Проверка тела запроса'):
                    expected_body = RESPONSE_BODY['block_blocked_user']['body']
                    actual_body = response.json()
                    assert actual_body.get('detail', None) == expected_body['detail'], f'Поле detail = ' \
                                                                                       f'{actual_body.get("detail", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["detail"]}'
                    assert actual_body.get('status', None) == expected_body['status'], f'Поле status = ' \
                                                                                       f'{actual_body.get("status", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["status"]}'

                with allure.step('Проверка кода ответа'):
                    expected_code = RESPONSE_BODY['block_blocked_user']['code']
                    assert response.status_code == expected_code, f'Код ответа {response.status_code}!= {expected_code}'

            @allure.title('Блокировка несуществующего пользователя')
            @pytest.mark.API
            def test_block_non_existing_user(self, block_non_existing_user):
                user, response, db_len = block_non_existing_user

                db_data = self.sql_client.get_all_table_data(table_model=TestUserModel)

                with allure.step('Проверка записанных в БД данных'):
                   assert len(db_data) == db_len

                with allure.step('Проверка тела запроса'):
                    expected_body = RESPONSE_BODY['block_non_existing_user']['body']
                    actual_body = response.json()
                    assert actual_body.get('detail', None) == expected_body['detail'], f'Поле detail = ' \
                                                                                       f'{actual_body.get("detail", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["detail"]}'
                    assert actual_body.get('status', None) == expected_body['status'], f'Поле status = ' \
                                                                                       f'{actual_body.get("status", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["status"]}'

                with allure.step('Проверка кода ответа'):
                    expected_code = RESPONSE_BODY['block_non_existing_user']['code']
                    assert response.status_code == expected_code, f'Код ответа {response.status_code}!= {expected_code}'

        @allure.feature('Разблокировка пользователя - POST /api/user/<username>/accept')
        class TestUnblockUser(BaseApiTest):

            @allure.title('Разблокировка заблокированного пользователя')
            @pytest.mark.API
            def test_unblock_blocked_user(self, unblock_blocked_user):
                user, response = unblock_blocked_user
                db_data = self.sql_client.get_table_data(table_model=TestUserModel,
                                                         email=user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data.name == user['name'], f'Имена не совпадают! Подробности в отчете'
                    assert db_data.surname == user['surname'], f'Фамилии не совпадают! Подробности в отчете'
                    assert db_data.middle_name == user['middle_name'], f'Отчества не совпадают! Подробности в отчете'
                    assert db_data.username == user['username'], f'Юзернеймы не совпадают! Подробности в отчете'
                    assert db_data.password == user['password'], f'Пароли не совпадают! Подробности в отчете'
                    assert db_data.email == user['email'], f'Почты не совпадают! Подробности в отчете'
                    assert db_data.access == 1

                with allure.step('Проверка тела запроса'):
                    expected_body = RESPONSE_BODY['unblock_blocked_user']['body']
                    actual_body = response.json()
                    assert actual_body.get('detail', None) == expected_body['detail'], f'Поле detail = ' \
                                                                                       f'{actual_body.get("detail", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["detail"]}'
                    assert actual_body.get('status', None) == expected_body['status'], f'Поле status = ' \
                                                                                       f'{actual_body.get("status", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["status"]}'

                with allure.step('Проверка кода ответа'):
                    expected_code = RESPONSE_BODY['unblock_blocked_user']['code']
                    assert response.status_code == expected_code, f'Код ответа {response.status_code}!= {expected_code}'

            @allure.title('Разблокировка разблокированного пользователя')
            @pytest.mark.API
            def test_unblock_active_user(self, unblock_active_user):
                user, response = unblock_active_user
                db_data = self.sql_client.get_table_data(table_model=TestUserModel,
                                                         email=user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data.name == user['name'], f'Имена не совпадают! Подробности в отчете'
                    assert db_data.surname == user['surname'], f'Фамилии не совпадают! Подробности в отчете'
                    assert db_data.middle_name == user['middle_name'], f'Отчества не совпадают! Подробности в отчете'
                    assert db_data.username == user['username'], f'Юзернеймы не совпадают! Подробности в отчете'
                    assert db_data.password == user['password'], f'Пароли не совпадают! Подробности в отчете'
                    assert db_data.email == user['email'], f'Почты не совпадают! Подробности в отчете'
                    assert db_data.access == 1

                with allure.step('Проверка тела запроса'):
                    expected_body = RESPONSE_BODY['unblock_active_user']['body']
                    actual_body = response.json()
                    assert actual_body.get('detail', None) == expected_body['detail'], f'Поле detail = ' \
                                                                                       f'{actual_body.get("detail", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["detail"]}'
                    assert actual_body.get('status', None) == expected_body['status'], f'Поле status = ' \
                                                                                       f'{actual_body.get("status", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["status"]}'

                with allure.step('Проверка кода ответа'):
                    expected_code = RESPONSE_BODY['unblock_active_user']['code']
                    assert response.status_code == expected_code, f'Код ответа {response.status_code}!= {expected_code}'

            @allure.title('Разблокировка несуществующего пользователя')
            @pytest.mark.API
            def test_block_non_existing_user(self, unblock_non_existing_user):
                user, response, db_len = unblock_non_existing_user
                db_data = self.sql_client.get_all_table_data(table_model=TestUserModel)

                with allure.step('Проверка записанных в БД данных'):
                    assert len(db_data) == db_len

                with allure.step('Проверка тела запроса'):
                    expected_body = RESPONSE_BODY['unblock_non_existing_user']['body']
                    actual_body = response.json()
                    assert actual_body.get('detail', None) == expected_body['detail'], f'Поле detail = ' \
                                                                                       f'{actual_body.get("detail", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["detail"]}'
                    assert actual_body.get('status', None) == expected_body['status'], f'Поле status = ' \
                                                                                       f'{actual_body.get("status", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["status"]}'

                with allure.step('Проверка кода ответа'):
                    expected_code = RESPONSE_BODY['unblock_non_existing_user']['code']
                    assert response.status_code == expected_code, f'Код ответа {response.status_code}!= {expected_code}'

        @allure.feature('Получение статуса приложения - GET /status')
        class TestGetStatus(BaseApiTest):

            @allure.title('Получение статуса')
            @pytest.mark.API
            def test_get_status(self):
                response = self.api_client.get_status()

                with allure.step('Проверка тела запроса'):
                    expected_body = RESPONSE_BODY['get_status']['body']
                    actual_body = response.json()
                    assert actual_body.get('status', None) == expected_body['status'], f'Поле status = ' \
                                                                                       f'{actual_body.get("status", None)}' \
                                                                                       f'не совпадает с ожидаемым - ' \
                                                                                       f'{expected_body["status"]}'

                with allure.step('Проверка кода ответа'):
                    expected_code = RESPONSE_BODY['get_status']['code']
                    assert response.status_code == expected_code, f'Код ответа {response.status_code}!= {expected_code}'

    @allure.suite('Запросы к Mock-серверу')
    class TestMockService:
        pass
