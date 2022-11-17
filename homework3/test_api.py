import pytest

from base import ApiBase


class TestSegments(ApiBase):
    @pytest.mark.API
    def test_games_segment_creation(self, new_games_segment):
        games_segment = new_games_segment

        assert self.check_segment_in_segments_list(segment_id=games_segment.segment_id,
                                                   segment_name=games_segment.name)

    @pytest.mark.API
    def test_vk_segment_creation(self, new_vk_segment):
        vk_segment = new_vk_segment

        assert self.check_segment_in_segments_list(segment_id=vk_segment.segment_id,
                                                   segment_name=vk_segment.name)
