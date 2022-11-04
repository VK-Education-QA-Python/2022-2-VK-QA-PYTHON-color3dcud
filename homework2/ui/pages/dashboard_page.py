from ui.locators import locators
from ui.pages.base_page import BasePage


class DashboardPage(BasePage):
    locators = locators.DashboardPageLocators()
    url = 'https://target-sandbox.my.com/dashboard'

    def go_to_new_campaign_page(self):
        from ui.pages.new_campaign_page import NewCampaignPage
        self.click_button(locator=self.locators.CREATE_CAMPAIGN_BUTTON)
        return NewCampaignPage(driver=self.driver)
