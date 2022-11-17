import pytest
import time
import random
import os
from base import BaseCase


class TestCampaignPage(BaseCase):
    video_file = 'campaign_video.mp4'
    icon_file = 'logo.png'

    @pytest.mark.UI
    def test_create_campaign(self, files_path):
        self.new_campaign_page.driver.get(self.new_campaign_page.url)
        self.new_campaign_page.click_button(self.new_campaign_page.locators.COVERAGE_CAMPAIGN)
        campaign_link = 'https://stepik.org/'
        self.new_campaign_page.change_input(locator=self.new_campaign_page.locators.LINK_TO_PRODUCT,
                                            new_value=campaign_link)
        campaign_name = 'Test from selenium, ID = ' + str(random.randint(100, 999))
        self.new_campaign_page.change_input(locator=self.new_campaign_page.locators.CAMPAIGN_NAME,
                                            new_value=campaign_name)
        self.new_campaign_page.click_button(self.new_campaign_page.locators.BUDGET_LEFT_BAR)
        day_budget = random.randint(1, 10000)
        total_budget = day_budget * 100
        self.new_campaign_page.change_input(locator=self.new_campaign_page.locators.DAY_BUDGET_FIELD,
                                            new_value=day_budget)
        self.new_campaign_page.change_input(locator=self.new_campaign_page.locators.TOTAL_BUDGET_FIELD,
                                            new_value=total_budget)
        self.new_campaign_page.click_button(self.new_campaign_page.locators.SUPERVIDEO)
        time.sleep(10)
        icon_path = files_path + self.icon_file
        video_path = files_path + self.video_file
        self.new_campaign_page.upload_file(locator=self.new_campaign_page.locators.ICON_INPUT_BUTTON,
                                           file_path=icon_path)
        self.new_campaign_page.upload_file(locator=self.new_campaign_page.locators.VIDEO_INPUT_BUTTON,
                                           file_path=video_path)
        self.new_campaign_page.wait_supervideo_loaded()
        self.new_campaign_page.change_input(locator=self.new_campaign_page.locators.CAMPAIGN_HEADER_FIELD,
                                            new_value='New era of tests')
        self.new_campaign_page.change_input(locator=self.new_campaign_page.locators.AD_TEXT,
                                            new_value='Hello, world!')
        self.new_campaign_page.save_campaign()

        assert self.dashboard_page.is_campaign_present(campaign_name=campaign_name)


class TestSegmentsPage(BaseCase):
    vk_url = 'https://vk.com/vkedu'

    @pytest.mark.UI
    def test_new_game_segment_creation(self):
        segment_name = 'Test segment creation from selenium, ID = ' + str(random.randint(100, 999))
        self.new_segment_page.driver.get(self.new_segment_page.url)
        self.new_segment_page.add_new_segment(segment_element_locator=self.new_segment_page.locators.GAMES_AND_APPS,
                                              segment_name=segment_name)
        assert self.segments_page.is_segment_present(segment_name=segment_name)

    @pytest.mark.UI
    def test_new_vk_segment_create_and_delete(self):
        self.groups_page.driver.get(self.groups_page.url)
        self.groups_page.add_vk_group(vk_url=self.vk_url)
        self.groups_page.go_to_segments_page()
        self.segments_page.go_to_new_segment_page()
        segment_name = 'Test VK segment from selenium, ID = ' + str(random.randint(100, 999))
        self.new_segment_page.add_new_segment(segment_element_locator=self.new_segment_page.locators.VK_OK,
                                              segment_name=segment_name)
        assert self.segments_page.is_segment_present(segment_name=segment_name)
        self.segments_page.delete_segment(segment_name=segment_name)
        assert self.segments_page.is_segment_present(segment_name=segment_name, timeout=2) is False
        self.segments_page.go_to_groups_page()
        self.groups_page.delete_last_group()
        assert self.groups_page.is_group_present(vk_url=self.vk_url, timeout=2) is False
