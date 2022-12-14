import allure

from ui.pages.base_page import BasePage
from ui.locators.login_page_locators import LoginPageLocators

from static.app_config import APP_CONFIG
from static.credentials import CREDENTIALS


class LoginPage(BasePage):
    url = f'{APP_CONFIG["APP_URL"]}/login'
    locators = LoginPageLocators()

    @allure.step("Вводим данные пользователя")
    def fill_creds(self, username=CREDENTIALS['main']['username'], password=CREDENTIALS['main']['password']):
        self.change_input(locator=self.locators.USERNAME_INPUT_FIELD, value=username)
        self.change_input(locator=self.locators.PASSWORD_INPUT_FIELD, value=password)
        self.click_button(locator=self.locators.LOGIN_BUTTON)

