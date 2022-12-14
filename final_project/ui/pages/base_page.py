import time

import allure
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import *

from static.ui.timeouts import *


class PageNotOpenedException(Exception):
    pass


class BasePage:
    CLICK_RETRY = 3
    locators = None
    url = None

    def __init__(self, driver):
        self.driver = driver

    def go_to_page(self, is_opened=True):
        self.driver.get(self.url)
        if is_opened:
            self.is_opened()
    @allure.step("Проверяем открытие страницы")
    def is_opened(self, timeout=15):
        started = time.time()
        if self.url is not None:
            while time.time() - started < timeout:
                if self.driver.current_url == self.url:
                    return True
            raise PageNotOpenedException(f'{self.url} dont open in {timeout}sec, '
                                         f'current url {self.driver.current_url}')

    def wait(self, timeout=None):
        if timeout is None:
            timeout = DEFAULT_WAIT_TIMEOUT
        return WebDriverWait(self.driver, timeout=timeout)

    @allure.step("Ждем существования элемента")
    def wait_presence_of_element(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    @allure.step("Ждем существования и видимости элемента")
    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.visibility_of_element_located(locator))

    @allure.step("Ищем невидимый элемент")
    def find_invisibility_element(self, locator, timeout=None):
        return self.wait(timeout).until(EC.invisibility_of_element_located(locator))

    @allure.step("Очищаем и заполняем поле")
    def change_input(self, locator, value, timeout=None):
        field = self.find(locator, timeout=timeout)
        field.clear()
        field.send_keys(value)

    @allure.step("Кликаем по полю")
    def click_button(self, locator, timeout=None):
        for i in range(self.CLICK_RETRY):
            try:
                button = self.find(locator, timeout=timeout)
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
