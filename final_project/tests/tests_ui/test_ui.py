import random
import time

import pytest

from tests.tests_ui.base_ui import BaseCase
from utils.random_credentials import random_creds
from static.credentials import CREDENTIALS
from ui.locators.login_page_locators import LoginPageLocators
from ui.locators.registration_page_locators import RegistrationPageLocators
from utils.user_builder import *
from mysql.models.test_user_model import TestUserModel
from static.app_config import APP_CONFIG


@allure.parent_suite('Тестирование UI')
class TestUI:
    @allure.suite('Тестирование страницы Login Page')
    class TestLoginPage(BaseCase):

        @allure.title('Успешная авторизация пользователя')
        @pytest.mark.UI
        def test_authorization(self):
            self.login_page.go_to_page()
            self.login_page.fill_creds()

            assert self.driver.current_url == self.main_page.url

        @allure.title('Авторизация с некорректными данными пользователя (несуществующие username + pass')
        @pytest.mark.UI
        def test_wrong_auth(self):
            self.login_page.go_to_page()
            creds = random_creds()
            self.login_page.fill_creds(username=creds['username'], password=creds['password'])

            error_message = self.login_page.find(locator=self.login_page.locators.ERROR_MESSAGE)

            assert self.driver.current_url == self.login_page.url
            assert error_message
            assert error_message.text == 'Invalid username or password'

        @allure.title('Авторизация заблокированным пользователем')
        @pytest.mark.UI
        def test_login_block_user(self):
            self.login_page.go_to_page()
            creds = CREDENTIALS['blocked_user']
            self.login_page.fill_creds(username=creds['username'], password=creds['password'])

            error_message = self.login_page.find(locator=self.login_page.locators.ERROR_MESSAGE)

            assert self.driver.current_url == self.login_page.url
            assert error_message
            assert error_message.text == 'Ваша учетная запись заблокирована'

        @allure.title('Авторизация с пустыми username + pass')
        @pytest.mark.UI
        def test_login_null_cred(self):
            self.login_page.go_to_page()
            self.login_page.fill_creds(username='', password='')

            validation = self.login_page.find(locator=self.login_page.locators.USERNAME_INPUT_FIELD)
            message = validation.get_attribute('validationMessage')

            assert self.driver.current_url == self.login_page.url
            assert message == f'Заполните это поле.'

        @allure.feature('Тестирование валидации полей на странице Login Page')
        class TestLoginFieldsValidation(BaseCase):
            @allure.title('Проверка валидации username')
            @pytest.mark.UI
            def test_username_validation(self):
                self.login_page.go_to_page()
                self.login_page.fill_creds(username='qwe', password='test')
                validation = self.login_page.find(locator=self.login_page.locators.USERNAME_INPUT_FIELD)
                message = validation.get_attribute('validationMessage')
                assert message == f'Минимально допустимое количество символов: 6. Длина текста сейчас: 3.'
                assert self.driver.current_url == self.login_page.url

        @allure.feature('Тестирование значений плейсхолдеров на странице Login Page')
        class TestLoginPagePlacehodlers(BaseCase):

            @allure.title('Тестирование плейсхолдеров Login Page')
            @pytest.mark.UI
            @pytest.mark.parametrize('field, placeholder', [(LoginPageLocators.USERNAME_INPUT_FIELD, 'Username'),
                                                            (LoginPageLocators.PASSWORD_INPUT_FIELD, 'Password')])
            def test_placehodlers(self, field, placeholder):
                self.login_page.go_to_page()
                field = self.login_page.find(locator=field)
                with allure.step(f'Проверка плейсхолдера для поля {field}'):
                    assert field.get_attribute('placeholder') == placeholder

        @allure.title('Переход на страницу Регистрации')
        @pytest.mark.UI
        def test_go_to_registration(self):
            self.login_page.go_to_page()
            self.login_page.click_button(locator=self.login_page.locators.CREATE_ACCOUNT_BUTTON)

            assert self.driver.current_url == self.registration_page.url

    @allure.suite('Тестирование страницы Registration Page')
    class TestRegistrationPage(BaseCase):
        @allure.feature('Тестирование регистрации пользователя на странице Registration Page')
        class TestUserRegistration(BaseCase):

            @allure.title('Регистрация пользователя со всеми данными')
            @pytest.mark.UI
            def test_reg_full_user(self):
                self.registration_page.go_to_page()

                user = full_user()
                self.registration_page.fill_user_info(user=user)

                db_data = self.mysql_client.get_table_data(table_model=TestUserModel, email=user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data.name == user['name'], f'Имена не совпадают! Подробности в отчете'
                    assert db_data.surname == user['surname'], f'Фамилии не совпадают! Подробности в отчете'
                    assert db_data.middle_name == user['middle_name'], f'Отчества не совпадают! Подробности в отчете'
                    assert db_data.username == user['username'], f'Юзернеймы не совпадают! Подробности в отчете'
                    assert db_data.password == user['password'], f'Пароли не совпадают! Подробности в отчете'
                    assert db_data.email == user['email'], f'Почты не совпадают! Подробности в отчете'

                assert self.driver.current_url == self.main_page.url

            @allure.title('Регистрация пользователя без имени')
            @pytest.mark.UI
            def test_reg_user_without_name(self):
                self.registration_page.go_to_page()

                user = full_user()
                user['name'] = ''

                self.registration_page.fill_user_info(user=user)
                db_data = self.mysql_client.get_table_data(table_model=TestUserModel, email=user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data is None

                message = self.registration_page.get_validation_message(locator=self.registration_page.locators.NAME_INPUT)

                assert self.driver.current_url == self.registration_page.url
                assert message == 'Заполните это поле.'

            @allure.title('Регистрация пользователя без фамилии')
            @pytest.mark.UI
            def test_reg_user_without_surname(self):
                self.registration_page.go_to_page()

                user = full_user()
                user['surname'] = ''

                self.registration_page.fill_user_info(user=user)
                db_data = self.mysql_client.get_table_data(table_model=TestUserModel, email=user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data is None

                message = self.registration_page.get_validation_message(locator=
                                                                        self.registration_page.locators.SURNAME_INPUT)

                assert self.driver.current_url == self.registration_page.url
                assert message == 'Заполните это поле.'

            @allure.title('Регистрация пользователя без отчества')
            @pytest.mark.UI
            def test_reg_user_without_middle_name(self):
                self.registration_page.go_to_page()

                user = full_user()
                user['middle_name'] = ''

                self.registration_page.fill_user_info(user=user)
                db_data = self.mysql_client.get_table_data(table_model=TestUserModel, email=user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data.name == user['name'], f'Имена не совпадают! Подробности в отчете'
                    assert db_data.surname == user['surname'], f'Фамилии не совпадают! Подробности в отчете'
                    assert db_data.middle_name is None, f'Отчества не совпадают! Подробности в отчете'
                    assert db_data.username == user['username'], f'Юзернеймы не совпадают! Подробности в отчете'
                    assert db_data.password == user['password'], f'Пароли не совпадают! Подробности в отчете'
                    assert db_data.email == user['email'], f'Почты не совпадают! Подробности в отчете'


                assert self.driver.current_url == self.main_page.url

            @allure.title('Регистрация пользователя без имени пользователя')
            @pytest.mark.UI
            def test_reg_user_without_username(self):
                self.registration_page.go_to_page()

                user = full_user()
                user['username'] = ''

                self.registration_page.fill_user_info(user=user)
                db_data = self.mysql_client.get_table_data(table_model=TestUserModel, email=user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data is None

                message = self.registration_page.get_validation_message(locator=
                                                                        self.registration_page.locators.USERNAME_INPUT)

                assert self.driver.current_url == self.registration_page.url
                assert message == 'Заполните это поле.'

            @allure.title('Регистрация пользователя без почты')
            @pytest.mark.UI
            def test_reg_user_without_email(self):
                self.registration_page.go_to_page()

                user = full_user()
                user['email'] = ''

                self.registration_page.fill_user_info(user=user)
                db_data = self.mysql_client.get_table_data(table_model=TestUserModel, username=user['username'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data is None

                assert self.driver.current_url == self.registration_page.url
                assert self.registration_page.find(locator=self.registration_page.locators.EMAIL_LENGTH_MESSAGE)

            @allure.title('Регистрация пользователя без пароля')
            @pytest.mark.UI
            def test_reg_user_without_password(self):
                self.registration_page.go_to_page()

                user = full_user()
                user['password'] = ''

                self.registration_page.fill_user_info(user=user)
                db_data = self.mysql_client.get_table_data(table_model=TestUserModel, email=user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data is None

                message = self.registration_page.get_validation_message(locator=
                                                                        self.registration_page.locators.PASSWORD_INPUT)

                assert self.driver.current_url == self.registration_page.url
                assert message == 'Заполните это поле.'

            @allure.title('Регистрация пользователя без подтверждения пароля')
            @pytest.mark.UI
            def test_reg_user_without_password_repeat(self):
                self.registration_page.go_to_page()

                user = full_user()

                self.registration_page.fill_user_info(user=user, repeat_pass=False)
                db_data = self.mysql_client.get_table_data(table_model=TestUserModel, email=user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data is None

                assert self.driver.current_url == self.registration_page.url
                assert self.registration_page.find(locator=self.registration_page.locators.DIFF_PASSWORDS_MESSAGE)

            @allure.title('Регистрация пользователя без чек-бокса "SDET..."')
            @pytest.mark.UI
            def test_reg_user_without_check_box(self):
                self.registration_page.go_to_page()

                user = full_user()

                self.registration_page.fill_user_info(user=user, check_box=False)
                db_data = self.mysql_client.get_table_data(table_model=TestUserModel, email=user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data is None

                message = self.registration_page.get_validation_message(locator=
                                                                        self.registration_page.locators.SDET_CHECKBOX)

                assert self.driver.current_url == self.registration_page.url
                assert message == 'Чтобы продолжить, установите этот флажок.'

        @allure.feature('Тестирование gktqc[jklthjd на странице Registration Page')
        class TestRegistrationPagePlaceholders(BaseCase):
            @allure.title('Проверка плейсхолдеров Registration Page')
            @pytest.mark.UI
            @pytest.mark.parametrize('field, placeholder', [(RegistrationPageLocators.NAME_INPUT, 'Name'),
                                                            (RegistrationPageLocators.SURNAME_INPUT, 'Surname'),
                                                            (RegistrationPageLocators.MIDDLE_NAME_INPUT, 'Middlename'),
                                                            (RegistrationPageLocators.USERNAME_INPUT, 'Username'),
                                                            (RegistrationPageLocators.EMAIL_INPUT, 'Email'),
                                                            (RegistrationPageLocators.PASSWORD_INPUT, 'Password'),
                                                            (RegistrationPageLocators.REPEAT_PASS_INPUT, 'Repeat password')
                                                            ])
            def test_placehodlers_registration_page(self, field, placeholder):
                self.registration_page.go_to_page()
                field = self.login_page.find(locator=field)

                with allure.step(f'Проверяем плейсхолдер {field}'):
                    assert field.get_attribute('placeholder') == placeholder

        @allure.feature('Тестирование регистрации существующего пользователя на странице Registration Page')
        class TestRegisterExistingUsers(BaseCase):

            @allure.title('Регистрация пользователя с существующим username')
            @pytest.mark.UI
            def test_reg_existing_username(self):
                self.registration_page.go_to_page()

                user = full_user()
                user['username'] = 'test_user'

                self.registration_page.fill_user_info(user=user)
                db_data = self.mysql_client.get_table_data(table_model=TestUserModel, email=user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data is None

                assert self.driver.current_url == self.registration_page.url
                assert self.registration_page.find(locator=self.registration_page.locators.USER_ALREADY_EXISTS_MESSAGE)

            @allure.title('Регистрация пользователя с существующим email')
            @pytest.mark.UI
            def test_req_existing_email(self):
                self.registration_page.go_to_page()

                user = full_user()
                user['email'] = 'test@test.qa'

                self.registration_page.fill_user_info(user=user)
                db_data = self.mysql_client.get_table_data(table_model=TestUserModel, username=user['username'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data is None

                message = self.registration_page.find(locator=
                                                      self.registration_page.locators.EMAIL_ALREADY_EXISTS_MESSAGE).text
                assert self.driver.current_url == self.registration_page.url
                assert message == 'Email already exists'

        @allure.title('Переход на страницу Login Page')
        @pytest.mark.UI
        def test_go_to_login_page(self):
            self.registration_page.go_to_page()
            self.registration_page.click_button(locator=self.registration_page.locators.LOGIN_BUTTON)

            assert self.driver.current_url == self.login_page.url

        @allure.feature('Тестирование валидации полей на странице Registration Page')
        class TestRegistrationValidation(BaseCase):

            # Len = 1 -> Change Message
            @allure.title('Проверка минимальной длины username')
            @pytest.mark.UI
            def test_min_len_username(self):
                self.registration_page.go_to_page()
                user = full_user()
                username = 'u' * random.randint(1, 5)
                user['username'] = username

                self.registration_page.fill_user_info(user=user)
                db_data = self.mysql_client.get_table_data(table_model=TestUserModel, email=user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data is None

                message = self.registration_page.get_validation_message(locator=
                                                                        self.registration_page.locators.USERNAME_INPUT)

                assert self.driver.current_url == self.registration_page.url
                assert message == f'Минимально допустимое количество символов: 6. Длина текста сейчас: {len(username)}.'

            @allure.title('Проверка минимальной длины email')
            @pytest.mark.UI
            def test_min_len_email(self):
                self.registration_page.go_to_page()
                user = full_user()
                email = 'q@q.a'
                user['email'] = email

                self.registration_page.fill_user_info(user=user)
                db_data = self.mysql_client.get_table_data(table_model=TestUserModel, email=user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data is None

                message = self.registration_page.get_validation_message(locator=
                                                                        self.registration_page.locators.EMAIL_INPUT)

                assert self.driver.current_url == self.registration_page.url
                assert message == f'Минимально допустимое количество символов: 6. Длина текста сейчас: {len(email)}.'
                time.sleep(3)

            @allure.title('Проверка валидации по маске email')
            @pytest.mark.UI
            def test_email_schema(self):
                self.registration_page.go_to_page()
                user = full_user()
                email = 'qaqaqaqa'
                user['email'] = email

                self.registration_page.fill_user_info(user=user)
                db_data = self.mysql_client.get_table_data(table_model=TestUserModel, email=user['email'])

                with allure.step('Проверка записанных в БД данных'):
                    assert db_data is None

                message = self.registration_page.get_validation_message(locator=
                                                                        self.registration_page.locators.EMAIL_INPUT)

                assert self.driver.current_url == self.registration_page.url
                assert self.registration_page.find(locator=self.registration_page.locators.INVALID_EMAIL_MESSAGE)

    @allure.suite('Тестирование страницы Main Page')
    class TestMainPage(BaseCase):
        @allure.feature('Тестирование Main Page после авторизации')
        class TestMainPageAuthorized(BaseCase):

            @allure.title('Переход на страницу Main Page')
            @pytest.mark.UI
            def test_main_page(self):
                self.login_page.fill_creds()
                self.main_page.go_to_page()

                assert self.driver.current_url == self.main_page.url

            @allure.title('Проверка работы кнопки Домой (с жуком)')
            @pytest.mark.UI
            def test_main_page_home_button_with_bug(self):
                self.login_page.fill_creds()
                self.main_page.go_to_page()

                first_text = self.main_page.find(locator=self.main_page.locators.FOOTER_TEXT).text
                self.main_page.click_button(locator=self.main_page.locators.HOME_BUTTON_BUG)
                second_text = self.main_page.find(locator=self.main_page.locators.FOOTER_TEXT).text

                assert self.driver.current_url == self.main_page.url
                assert first_text != second_text

            @allure.title('Проверка работы кнопки Домой (без жука)')
            @pytest.mark.UI
            def test_main_page_home_button(self):
                self.login_page.fill_creds()
                self.main_page.go_to_page()

                first_text = self.main_page.find(locator=self.main_page.locators.FOOTER_TEXT).text
                self.main_page.click_button(locator=self.main_page.locators.HOME_BUTTON)
                second_text = self.main_page.find(locator=self.main_page.locators.FOOTER_TEXT).text

                assert self.driver.current_url == self.main_page.url
                assert first_text != second_text

            @allure.title('Проверка работы кнопки Python')
            @pytest.mark.UI
            def test_main_page_python_button(self):
                self.login_page.fill_creds()
                self.main_page.go_to_page()
                self.main_page.click_button(locator=self.main_page.locators.PYTHON_BUTTON)

                assert self.driver.current_url == 'https://www.python.org/'

            @allure.title('Проверка работы кнопки Python History')
            @pytest.mark.UI
            def test_main_page_python_history_button(self):
                self.login_page.fill_creds()
                self.main_page.go_to_page()
                self.main_page.click_python_history()

                assert self.driver.current_url == 'https://en.wikipedia.org/wiki/History_of_Python'

            @allure.title('Проверка работы кнопки About Flask')
            @pytest.mark.UI
            def test_main_page_about_flask_button(self):
                self.login_page.fill_creds()
                self.main_page.go_to_page()
                self.main_page.click_about_flask()

                assert self.driver.current_url == 'https://flask.palletsprojects.com/en/1.1.x/#'

            @allure.title('Проверка работы кнопки Download Centos')
            @pytest.mark.UI
            def test_main_page_centos_download(self):
                self.login_page.fill_creds()
                self.main_page.go_to_page()
                self.main_page.click_centos_download()

                assert self.driver.current_url == 'https://www.centos.org/download/'

            @allure.title('Проверка работы кнопки Network News')
            @pytest.mark.UI
            def test_main_page_network_news(self):
                self.login_page.fill_creds()
                self.main_page.go_to_page()
                self.main_page.click_network_news()

                assert self.driver.current_url == 'https://www.wireshark.org/news/'

            @allure.title('Проверка работы кнопки Network Download')
            @pytest.mark.UI
            def test_main_page_network_download(self):
                self.login_page.fill_creds()
                self.main_page.go_to_page()
                self.main_page.click_network_download()

                assert self.driver.current_url == 'https://www.wireshark.org/#download'

            @allure.title('Проверка работы кнопки Network Examples')
            @pytest.mark.UI
            def test_main_page_network_examples(self):
                self.login_page.fill_creds()
                self.main_page.go_to_page()
                self.main_page.click_network_examples()

                assert self.driver.current_url == 'https://hackertarget.com/tcpdump-examples/'

            @allure.title('Проверка работы кнопки API')
            @pytest.mark.UI
            def test_main_page_api(self):
                self.login_page.fill_creds()
                self.main_page.go_to_page()
                self.main_page.click_button(locator=self.main_page.locators.API_BUTTON)
                self.main_page.switch_page()

                assert self.driver.current_url == 'https://en.wikipedia.org/wiki/API'

            @allure.title('Проверка работы кнопки WWW')
            @pytest.mark.UI
            def test_main_page_www(self):
                self.login_page.fill_creds()
                self.main_page.go_to_page()
                self.main_page.click_button(locator=self.main_page.locators.WWW_BUTTON)
                self.main_page.switch_page()

                assert self.driver.current_url == 'https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/'

            @allure.title('Проверка работы кнопки SMTP')
            @pytest.mark.UI
            def test_main_page_smtp(self):
                self.login_page.fill_creds()
                self.main_page.go_to_page()
                self.main_page.click_button(locator=self.main_page.locators.SMTP_BUTTON)
                self.main_page.switch_page()

                assert self.driver.current_url == 'https://ru.wikipedia.org/wiki/SMTP'

            @allure.title('Проверка данных авторизованного пользователя')
            @pytest.mark.UI
            def test_logged_info(self):
                creds = CREDENTIALS['test_mock']
                self.login_page.fill_creds(username=creds['username'], password=creds['password'])

                logged_as = self.main_page.find(locator=self.main_page.locators.LOGGED_AS_TEXT).text
                user = self.main_page.find(locator=self.main_page.locators.USER_TEXT).text
                vk_id = self.main_page.find(locator=self.main_page.locators.VK_ID).text

                assert logged_as == f'Logged as {creds["username"]}'
                assert user == f'User: Mock Value'
                assert vk_id == 'VK ID: test_mock'

        @allure.feature('Тестирование Main Page без авторизации')
        class TestMainPageUnauthorized(BaseCase):

            @allure.title('Переход на Main Page без авторизации')
            @pytest.mark.UI
            def test_main_page_unauthorized(self):
                self.main_page.go_to_page(is_opened=False)

                assert self.driver.current_url == f'{APP_CONFIG["APP_URL"]}/login?next=/welcome/'
                assert self.login_page.find(locator=self.login_page.locators.ERROR_AUTH)
