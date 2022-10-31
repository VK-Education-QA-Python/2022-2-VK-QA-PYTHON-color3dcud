import pytest
from api.builder import Builder


class ApiBase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client):
        self.api_client = api_client
        self.builder = Builder()

        if self.authorize:
            self.api_client.get_csrf()

    def add_vk_group_to_group_list(self, url):
        vk_groups = self.api_client.get_vk_groups(full_url=url)
        vk_group_id = vk_groups['items'][0]['id']
        new_group = self.api_client.post_vk_group_add(vk_group_id=vk_group_id)
        new_group_id = new_group['items'][0]['id']
        self.check_vk_group_in_group_list(vk_group_id=new_group_id)
        return vk_group_id, new_group_id

    def check_vk_group_in_group_list(self, vk_group_id):
        found = False
        your_groups = self.api_client.get_your_vk_groups()

        for item in your_groups['items']:
            if item['id'] == vk_group_id:
                found = True
                break
        return found

    def check_segment_in_segments_list(self, segment_id):
        found = False
        your_segments = self.api_client.get_segments_list()

        for item in your_segments['items']:
            if item['id'] == segment_id:
                found = True
                break
        return found

    @pytest.fixture(scope='function')
    def new_vk_segment(self):
        vk_group = self.add_vk_group_to_group_list('https://vk.com/vkedu')
        segment_data = self.builder.segment(segment_type='vk', vk_group_id=vk_group[0])
        add_segment = self.api_client.post_segments_add(name=segment_data.name, relations=segment_data.relations)
        segment_id = add_segment['id']
        vk_group_id = vk_group[1]
        segment_data.segment_id = segment_id

        yield segment_data

        self.api_client.delete_segment(segment_id=segment_id)
        assert self.check_segment_in_segments_list(segment_id=segment_id) is False
        self.api_client.delete_vk_group(vk_group_id=vk_group_id)
        assert self.check_vk_group_in_group_list(vk_group_id=vk_group_id) is False

    @pytest.fixture(scope='function')
    def new_games_segment(self):
        segment_data = self.builder.segment(segment_type='games')
        add_segment = self.api_client.post_segments_add(name=segment_data.name, relations=segment_data.relations)
        segment_id = add_segment['id']
        segment_data.segment_id = segment_id

        yield segment_data

        self.api_client.delete_segment(segment_id=segment_id)
        assert self.check_segment_in_segments_list(segment_id=segment_id) is False
