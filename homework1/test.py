import random

import pytest

from base import BaseCase
from ui.locators import basic_locators


class TestOne(BaseCase):
    login_value = 'hsabuse@yandex.ru'
    pass_value = 'Qwe123-'

    @pytest.mark.UI
    def test_login(self):
        self.login(login=self.login_value, password=self.pass_value)
        assert self.find(basic_locators.USERNAME).text == self.login_value.upper()

    @pytest.mark.UI
    def test_logout(self):
        self.login(login=self.login_value, password=self.pass_value)
        assert self.find(basic_locators.USERNAME).text == self.login_value.upper()
        self.driver.refresh()
        self.click_button(basic_locators.HEADER_BUTTON)
        self.click_button(basic_locators.LOGOUT_BUTTON)
        assert self.is_present(basic_locators.MAIN_PAGE_DIV) == True
        assert self.driver.current_url == 'https://target-sandbox.my.com/'

    @pytest.mark.UI
    def test_negative_invalid_login_or_pass(self):
        self.login(login='111', password='111')
        assert self.is_present(basic_locators.LOGIN_FORM_MESSAGE_TITLE) == True
        assert self.is_present(basic_locators.LOGIN_FORM_MESSAGE_TEXT) == True
        assert self.find(basic_locators.LOGIN_FORM_MESSAGE_TITLE).text == 'Error'
        assert self.find(basic_locators.LOGIN_FORM_MESSAGE_TEXT).text == 'Invalid login or password'

    @pytest.mark.UI
    def test_negative_login_with_russian_credentials(self):
        self.login(login='почта', password='пароль')
        assert self.is_present(basic_locators.ENTER_EMAIL_OR_PHONE_ERROR) == True

    @pytest.mark.UI
    def test_change_profile_data(self):
        self.login(login=self.login_value, password=self.pass_value)
        self.click_button(basic_locators.PROFILE_BUTTON)
        new_inn = str(random.randint(1000000000, 9999999999))
        self.change_profile_field(basic_locators.INN_FIELD, new_inn)
        new_phone = ('+7999' + str(random.randint(1000000, 9999999)))
        self.change_profile_field(basic_locators.PHONE_FIELD, new_phone)
        self.click_button(basic_locators.SAVE_PROFILE_BUTTON)
        assert self.is_present(basic_locators.INFORMATION_CHANGED_MESSAGE) == True
        info = self.find(basic_locators.INFORMATION_CHANGED_MESSAGE)
        assert info.text == 'Информация успешно сохранена'

    @pytest.mark.UI
    @pytest.mark.parametrize('button, page_attr, url',
                             [(basic_locators.PROFILE_BUTTON, basic_locators.PROFILE_ATTR, '/profile'),
                              (basic_locators.BALANCE_BUTTON, basic_locators.BALANCE_ATTR, '/billing')])
    def test_header_buttons(self, button, page_attr, url):
        self.login(login=self.login_value, password=self.pass_value)
        self.click_button(button)
        assert self.driver.current_url.__contains__(url)
        assert self.is_present(page_attr) == True
