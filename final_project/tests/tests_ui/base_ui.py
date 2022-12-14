import os

import allure
import pytest
from _pytest.fixtures import FixtureRequest

from ui.fixtures import *
from ui.pages.login_page import LoginPage


class BaseCase:
    driver = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, logger, mysql_client, request: FixtureRequest):
        self.driver = driver
        self.config = config
        self.logger = logger
        self.login_page: LoginPage = (request.getfixturevalue('login_page'))
        self.registration_page: RegistrationPage = (request.getfixturevalue('registration_page'))
        self.main_page: MainPage = (request.getfixturevalue('main_page'))

        with allure.step("Выполняем коннект к БД и возвращаем объект соединения"):
            self.mysql_client = mysql_client

    @pytest.fixture(scope='function', autouse=True)
    def ui_report(self, driver, request, temp_dir):
        failed_test_count = request.session.testsfailed
        yield
        if request.session.testsfailed > failed_test_count:
            browser_logs = os.path.join(temp_dir, 'browser.log')
            with open(browser_logs, 'w') as f:
                for i in driver.get_log('browser'):
                    f.write(f"{i['level']} - {i['source']}\n{i['message']}\n")
            screenshot_path = os.path.join(temp_dir, 'failed.png')
            self.driver.save_screenshot(filename=screenshot_path)
            allure.attach.file(screenshot_path, 'failed.png', allure.attachment_type.PNG)
            with open(browser_logs, 'r') as f:
                allure.attach(f.read(), 'test.log', allure.attachment_type.TEXT)
