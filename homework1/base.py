import pytest
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from ui.locators import basic_locators

CLICK_RETRY = 3


class BaseCase:
    driver = None

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, driver):
        self.driver = driver

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 15
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.visibility_of_element_located(locator))

    def is_present(self, locator):
        try:
            self.find(locator)
            return True
        except NoSuchElementException:
            return False

    def click_button(self, locator):
        for i in range(CLICK_RETRY):
            try:
                button = self.find(locator)
                button.click()
                return
            except NoSuchElementException:
                if i == CLICK_RETRY - 1:
                    raise NoSuchElementException('Button was not found')
            except ElementClickInterceptedException:
                if i == CLICK_RETRY - 1:
                    raise ElementClickInterceptedException('Cant click the button')

    def login(self, login, password):
        self.click_button(basic_locators.HEADER_LOGIN_BUTTON)
        email = self.find(basic_locators.EMAIL_FIELD)
        email.clear()
        email.send_keys(login)
        password_field = self.find(basic_locators.PASSWORD_FIELD)
        password_field.clear()
        password_field.send_keys(password)
        self.find(basic_locators.WRAP_LOGIN_BUTTON).click()

    def logout_click(self):
        action = ActionChains(self.driver)
        header = self.find(basic_locators.HEADER_BUTTON)
        logout = self.find(basic_locators.LOGOUT_BUTTON)
        action.click(header).pause(1).click(logout).perform()

    def change_profile_field(self, locator, new_value):
        field = self.find(locator)
        field.clear()
        field.send_keys(new_value)
