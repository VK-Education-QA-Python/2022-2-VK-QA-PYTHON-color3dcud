import pytest

from base import ApiBase


class TestCampaign(ApiBase):
    @pytest.mark.skip('SKIP')
    def test_new_campaign_creation(self):
        pass


class TestSegments(ApiBase):
    @pytest.mark.API
    def test_games_segment_creation(self, new_games_segment):
        games_segment = new_games_segment
        self.check_segment_in_segments_list(segment_id=games_segment.segment_id)

    @pytest.mark.API
    def test_vk_segment_creation(self, new_vk_segment):
        vk_segment = new_vk_segment
        self.check_segment_in_segments_list(segment_id=vk_segment.segment_id)
