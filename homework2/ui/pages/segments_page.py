import time

from ui.locators import locators
from ui.pages.base_page import BasePage


class SegmentsPage(BasePage):
    locators = locators.SegmentsPageLocators()
    url = 'https://target-sandbox.my.com/segments/segments_list'

    def go_to_new_segment_page(self):
        from ui.pages.new_segment_page import NewSegmentPage
        self.click_button(self.locators.CREATE_SEGMENT)
        return NewSegmentPage(self.driver)

    def go_to_groups_page(self):
        from ui.pages.groups_page import GroupsPage
        self.click_button(self.locators.GROUPS_LIST)
        return GroupsPage(self.driver)

    def is_segment_present(self, segment_name, timeout=30):
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException
        from selenium.webdriver.common.by import By

        try:
            self.wait(timeout).until(EC.visibility_of_element_located((By.XPATH, f'//a[text()="{segment_name}"]')))
            return True
        except TimeoutException:
            return False

    def get_segment_id(self, segment_name, timeout=None):
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By

        elem = self.wait(timeout).until(EC.visibility_of_element_located((By.XPATH, f'//a[text()="{segment_name}"]')))
        href = elem.get_attribute('href')
        segment_id = href.split('/')[-1]
        return segment_id

    def delete_segment(self, segment_name):
        from selenium.webdriver.common.by import By
        segment_id = self.get_segment_id(segment_name=segment_name)
        self.click_button((By.XPATH, f'//div[contains(@data-test, "id-{segment_id}")]/div/input'))
        self.click_button(self.locators.MASS_ACTION)
        self.click_button(self.locators.REMOVE_MASS)
