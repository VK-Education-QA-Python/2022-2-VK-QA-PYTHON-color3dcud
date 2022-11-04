from ui.locators import locators
from ui.pages.segments_page import SegmentsPage


class NewSegmentPage(SegmentsPage):
    locators = locators.NewSegmentPageLocators()
    url = 'https://target-sandbox.my.com/segments/segments_list/new'

    def add_new_segment(self, segment_element_locator, segment_name):
        from ui.pages.segments_page import SegmentsPage

        self.click_button(segment_element_locator)
        self.click_button(self.locators.SEGMENT_CHECKBOX)
        self.click_button(self.locators.MODAL_ADD_SEGMENT_BUTTON)
        self.change_input(locator=self.locators.NEW_SEGMENT_NAME, new_value=segment_name)
        self.click_button(self.locators.FORM_ADD_SEGMENT_BUTTON)

        return SegmentsPage(driver=self.driver)
