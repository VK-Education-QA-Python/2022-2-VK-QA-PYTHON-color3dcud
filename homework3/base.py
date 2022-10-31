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
    def new_vk_edu_group(self):
        group_data = self.builder.group()
        all_vk_groups_by_url = self.api_client.get_vk_groups(full_url=group_data.group_url)
        vk_group_id = all_vk_groups_by_url['items'][0]['id']
        group_data.group_id = vk_group_id
        new_vk_group = self.api_client.post_vk_group_add(vk_group_id=vk_group_id)
        vk_group_id_list = new_vk_group['items'][0]['id']
        group_data.group_id_list = vk_group_id_list
        self.check_vk_group_in_group_list(vk_group_id=vk_group_id_list)

        yield group_data

        self.api_client.delete_vk_group(vk_group_id=vk_group_id_list)
        assert self.check_vk_group_in_group_list(vk_group_id=vk_group_id_list) is False

    @pytest.fixture(scope='function')
    def new_vk_segment(self, new_vk_edu_group):
        vk_group = new_vk_edu_group
        segment_data = self.builder.segment(segment_type='vk', vk_group_id=vk_group.group_id)
        add_segment = self.api_client.post_segments_add(name=segment_data.name, relations=segment_data.relations)
        segment_id = add_segment['id']
        segment_data.segment_id = segment_id

        yield segment_data

        self.api_client.delete_segment(segment_id=segment_id)
        assert self.check_segment_in_segments_list(segment_id=segment_id) is False

    @pytest.fixture(scope='function')
    def new_games_segment(self):
        segment_data = self.builder.segment(segment_type='games')
        add_segment = self.api_client.post_segments_add(name=segment_data.name, relations=segment_data.relations)
        segment_id = add_segment['id']
        segment_data.segment_id = segment_id

        yield segment_data

        self.api_client.delete_segment(segment_id=segment_id)
        assert self.check_segment_in_segments_list(segment_id=segment_id) is False
