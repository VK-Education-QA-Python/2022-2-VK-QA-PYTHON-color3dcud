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
        assert self.is_present(basic_locators.HEADER_BUTTON)

    @pytest.mark.UI
    def test_logout(self):
        self.login(login=self.login_value, password=self.pass_value)
        assert self.is_present(basic_locators.HEADER_BUTTON)
        self.driver.refresh()
        self.click_button(basic_locators.HEADER_BUTTON)
        self.click_button(basic_locators.LOGOUT_BUTTON)
        assert self.is_present(basic_locators.HEADER_LOGIN_BUTTON)

    @pytest.mark.UI
    def test_negative_invalid_login_or_pass(self):
        self.login(login='111', password='111')
        assert self.is_present(basic_locators.LOGIN_FORM_MESSAGE)

    @pytest.mark.UI
    def test_negative_login_with_russian_credentials(self):
        self.login(login='почта', password='пароль')
        assert self.is_present(basic_locators.ENTER_EMAIL_OR_PHONE_ERROR)

    @pytest.mark.UI
    def test_change_profile_data(self):
        self.login(login=self.login_value, password=self.pass_value)
        self.click_button(basic_locators.PROFILE_BUTTON)
        new_inn = str(random.randint(1000000000, 9999999999))
        self.change_profile_field(basic_locators.INN_FIELD, new_inn)
        new_phone = ('+7999' + str(random.randint(1000000, 9999999)))
        self.change_profile_field(basic_locators.PHONE_FIELD, new_phone)
        self.click_button(basic_locators.SAVE_PROFILE_BUTTON)
        assert self.is_present(basic_locators.INFORMATION_CHANGED_MESSAGE)

    @pytest.mark.UI
    @pytest.mark.parametrize('button, page_attr',
                             [(basic_locators.PROFILE_BUTTON, basic_locators.PROFILE_ATTR),
                              (basic_locators.BALANCE_BUTTON, basic_locators.BALANCE_ATTR)])
    def test_header_buttons(self, button, page_attr):
        self.login(login=self.login_value, password=self.pass_value)
        self.click_button(button)
        assert self.is_present(page_attr)
