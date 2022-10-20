import time

from ui.locators import locators
from ui.pages.segments_page import SegmentsPage


class GroupsPage(SegmentsPage):
    locators = locators.GroupsPage()
    url = 'https://target-sandbox.my.com/segments/groups_list'

    def add_vk_group(self, vk_url):
        self.change_input(locator=self.locators.SEARCH_INPUT,
                          new_value=vk_url)
        time.sleep(2)
        self.click_button(self.locators.SELECT_GROUPS)
        self.click_button(self.locators.ADD_GROUP)

    def wait_hide_confirm_modal(self, timeout=None):
        from selenium.webdriver.support import expected_conditions as EC

        self.wait(timeout).until(EC.invisibility_of_element_located(self.locators.DELETE_MODAL))

    def delete_last_group(self):
        self.find(self.locators.TABLE)
        self.click_button(self.locators.DELETE_GROUP)
        self.click_button(self.locators.CONFIRM_REMOVE)
        self.wait_hide_confirm_modal()

    def go_to_segments_page(self):
        from ui.pages.segments_page import SegmentsPage
        self.click_button(self.locators.SEGMENTS_LIST)
        return SegmentsPage(self.driver)

    def is_group_present(self, vk_url, timeout=30):
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException
        from selenium.webdriver.common.by import By

        try:
            self.wait(timeout).until(EC.visibility_of_element_located((By.XPATH, f'//a[@href="{vk_url}"]')))
            return True
        except TimeoutException:
            return False
