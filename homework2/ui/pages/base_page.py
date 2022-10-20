import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By

from ui.locators import locators


class PageNotOpenedException(Exception):
    pass


class BasePage(object):
    CLICK_RETRY = 3
    locators = locators.BasePageLocators()
    url = None

    def __init__(self, driver, check_opened=True):
        self.driver = driver
        self.check_opened = check_opened
        self.is_opened()

    def is_opened(self, timeout=15):
        if self.check_opened:
            started = time.time()
            if self.url is not None:
                while time.time() - started < timeout:
                    if self.driver.current_url == self.url:
                        return True
                raise PageNotOpenedException(f'{self.url} dont open in {timeout}sec, '
                                             f'current url {self.driver.current_url}')

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 15
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.visibility_of_element_located(locator))

    def click_button(self, locator, timeout=None):
        for i in range(self.CLICK_RETRY):
            try:
                button = self.find(locator)
                button.click()
                return
            except NoSuchElementException:
                if i == self.CLICK_RETRY - 1:
                    raise NoSuchElementException('Button was not found')
            except ElementClickInterceptedException:
                if i == self.CLICK_RETRY - 1:
                    raise ElementClickInterceptedException('Cant click the button')
            except TimeoutException:
                if i == self.CLICK_RETRY - 1:
                    raise TimeoutException('Button was not found')

    def is_element_visible(self, locator, timeout=None):
        try:
            self.find(locator=locator, timeout=timeout)
            return True
        except TimeoutException:
            return False

    def change_input(self, locator, new_value):
        field = self.find(locator)
        field.clear()
        field.send_keys(new_value)

    def upload_file(self, locator, file_path):
        upload_input = self.driver.find_element(*locator)
        upload_input.send_keys(file_path)

    def is_campaign_present(self, campaign_name, timeout=60):
        try:
            self.wait(timeout).until(EC.visibility_of_element_located((By.XPATH, f'//a[text()="{campaign_name}"]')))
            return True
        except NoSuchElementException:
            return False
