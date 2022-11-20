AUTH = 'https://auth-ac.my.com/auth'
CSRF_LOCATION = 'csrf/'
GET_VK_GROUPS_LOCATION = 'api/v2/vk_groups.json'
POST_VK_GROUP_ADD_LOCATION = 'api/v2/remarketing/vk_groups/bulk.json'
GET_YOUR_VK_GROUPS_LOCATION = 'api/v2/remarketing/vk_groups.json'
POST_SEGMENT_ADD_LOCATION = 'api/v2/remarketing/segments.json'
GET_SEGMENTS_LIST_LOCATION = 'api/v2/remarketing/segments.json'


def delete_vk_group_location(vk_group_id):
    return f'api/v2/remarketing/vk_groups/{vk_group_id}.json'


def delete_segment_location(segment_id):
    return f'api/v2/remarketing/segments/{segment_id}.json'
