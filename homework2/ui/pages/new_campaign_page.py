from selenium.webdriver.support import expected_conditions as EC

from ui.locators import locators
from ui.pages.base_page import BasePage


class NewCampaignPage(BasePage):
    locators = locators.NewCampaignPageLocators()
    url = 'https://target-sandbox.my.com/campaign/new'

    def wait_supervideo_loaded(self, timeout=60):
        return self.wait(timeout).until(EC.presence_of_element_located(self.locators.VIDEO_PREVIEW))

    def save_campaign(self):
        from ui.pages.dashboard_page import DashboardPage
        self.click_button(self.locators.SAVE_CAMPAIGN_BUTTON)
        return DashboardPage(self.driver, check_opened=False)
