from _pytest.fixtures import FixtureRequest

from ui.fixtures import *


class BaseCase:
    driver = None
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest):
        self.driver = driver
        self.config = config

        self.main_page: MainPage = (request.getfixturevalue('main_page'))
        if self.authorize:
            cookies = request.getfixturevalue('cookies')
            for cookie in cookies:
                self.driver.add_cookie(cookie)

            self.driver.refresh()
            self.dashboard_page: DashboardPage = (request.getfixturevalue('dashboard_page'))
            self.new_campaign_page: NewCampaignPage = (request.getfixturevalue('new_campaign_page'))
            self.segments_page: SegmentsPage = (request.getfixturevalue('segments_page'))
            self.new_segment_page: NewSegmentPage = (request.getfixturevalue('new_segment_page'))
            self.groups_page: GroupsPage = (request.getfixturevalue('groups_page'))
