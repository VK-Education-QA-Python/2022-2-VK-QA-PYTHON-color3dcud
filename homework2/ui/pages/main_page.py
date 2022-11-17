from ui.locators import locators
from ui.pages.base_page import BasePage


class MainPage(BasePage):
    locators = locators.MainPageLocators()
    url = 'https://target-sandbox.my.com/'

    def login(self, login, password):
        self.click_button(self.locators.HEADER_LOGIN_BUTTON)
        email = self.find(self.locators.EMAIL_FIELD)
        email.clear()
        email.send_keys(login)
        password_field = self.find(self.locators.PASSWORD_FIELD)
        password_field.clear()
        password_field.send_keys(password)
        self.find(self.locators.WRAP_LOGIN_BUTTON).click()
