GET_AUTH_HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://target-sandbox.my.com',
    'Referer': 'https://target-sandbox.my.com/'
}
GET_AUTH_PARAMS = {
    'lang': 'ru',
    'nosavelogin': 0
}
POST_VK_GROUP_ADD_PARAMS = {
    'fields': 'id,object_id,name,users_count,url'
}
GET_YOUR_VK_GROUPS_PARAMS = {
    'fields': 'id,object_id,name,users_count,url',
    'limit': 50
}
POST_SEGMENTS_ADD_PARAMS = {
    'fields': 'relations__object_type,relations__object_id,relations__params,'
              'relations__params__score,relations__id,relations_count,id,name,pass_condition,'
              'created,campaign_ids,users,flags'
}
POST_SEGMENTS_ADD_HEADERS = {
    'Content-Type': 'application/json'
}
GET_SEGMENTS_LIST_PARAMS = {
    'fields': 'relations__object_type,relations__object_id,relations__params,relations__params__score,'
              'relations__id,relations_count,id,name,pass_condition,created,campaign_ids,users,flags',
    'limit': 500
}


def get_auth_body(login, password):
    body = {
        'email': login,
        'password': password,
        'continue': 'https://target-sandbox.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email',
        'failure': 'https://account.my.com/login/'
    }

    return body


def get_vk_groups_params(full_url):
    params = {
        '_q': full_url
    }

    return params


def post_vk_group_add_body(vk_group_id):
    body = {
        'items': [
            {
                'object_id': vk_group_id
            }
        ]
    }

    return body


def post_segments_add_body(name, relations):
    body = {
        "name": name,
        "pass_condition": 1,
        "relations": relations,
        "logicType": "rule"
    }

    return body
