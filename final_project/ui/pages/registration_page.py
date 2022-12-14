from static.app_config import APP_CONFIG
from ui.locators.registration_page_locators import RegistrationPageLocators
from ui.pages.base_page import BasePage


class RegistrationPage(BasePage):
    url = f'{APP_CONFIG["APP_URL"]}/reg'
    locators = RegistrationPageLocators()

    def fill_user_info(self, user: dict, check_box=True, repeat_pass=True):
        self.change_input(locator=self.locators.NAME_INPUT, value=user['name'])
        self.change_input(locator=self.locators.SURNAME_INPUT, value=user['surname'])
        self.change_input(locator=self.locators.MIDDLE_NAME_INPUT, value=user['middle_name'])
        self.change_input(locator=self.locators.USERNAME_INPUT, value=user['username'])
        self.change_input(locator=self.locators.EMAIL_INPUT, value=user['email'])
        self.change_input(locator=self.locators.PASSWORD_INPUT, value=user['password'])

        if repeat_pass:
            self.change_input(locator=self.locators.REPEAT_PASS_INPUT, value=user['password'])
        else:
            self.change_input(locator=self.locators.REPEAT_PASS_INPUT, value='')
        if check_box:
            self.click_button(locator=self.locators.SDET_CHECKBOX)

        self.click_button(locator=self.locators.REGISTER_BUTTON)

    def get_validation_message(self, locator):
        element = self.find(locator=locator)
        message = element.get_attribute('validationMessage')

        return message
