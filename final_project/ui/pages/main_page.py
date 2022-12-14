import time

import allure
from selenium.webdriver import ActionChains

from static.app_config import APP_CONFIG
from ui.locators.main_page_locators import MainPageLocators
from ui.pages.base_page import BasePage


class MainPage(BasePage):
    url = f'{APP_CONFIG["APP_URL"]}/welcome/'
    locators = MainPageLocators()

    def click_home_with_bug(self):
        self.click_button(locator=self.locators.HOME_BUTTON_BUG)

    def hover_on_element(self, locator):
        element = self.find(locator=locator)
        actions = ActionChains(self.driver)
        with allure.step(f'Наводим на элемент - {locator}'):
            actions.move_to_element(to_element=element).perform()

    def switch_page(self):
        window_after = self.driver.window_handles[1]
        self.driver.switch_to.window(window_after)

    def click_python_history(self):
        self.hover_on_element(locator=self.locators.PYTHON_BUTTON)
        self.click_button(locator=self.locators.PYTHON_HISTORY_BUTTON)

    def click_about_flask(self):
        self.hover_on_element(locator=self.locators.PYTHON_BUTTON)
        self.click_button(locator=self.locators.ABOUT_FLASK_BUTTON)
        self.switch_page()

    def click_centos_download(self):
        self.hover_on_element(locator=self.locators.LINUX_BUTTON)
        self.click_button(locator=self.locators.CENTOS_DOWNLOAD_BUTTON)
        self.switch_page()

    def click_network_news(self):
        self.hover_on_element(locator=self.locators.NETWORK_BUTTON)
        self.click_button(locator=self.locators.NETWORK_NEWS_BUTTON)
        self.switch_page()

    def click_network_download(self):
        self.hover_on_element(locator=self.locators.NETWORK_BUTTON)
        self.click_button(locator=self.locators.NETWORK_DOWNLOAD_BUTTON)
        self.switch_page()

    def click_network_examples(self):
        self.hover_on_element(locator=self.locators.NETWORK_BUTTON)
        self.click_button(locator=self.locators.NETWORK_EXAMPLES_BUTTON)
        self.switch_page()
