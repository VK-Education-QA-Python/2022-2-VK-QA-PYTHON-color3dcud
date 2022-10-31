import requests
from urllib.parse import urljoin


class ApiClientException(Exception):
    pass


class ResponseStatusCodeException(Exception):
    pass


class ResponseErrorException(Exception):
    pass


class ResponseJsonParseError(Exception):
    pass


class ApiClient:

    def __init__(self, base_url: str, login: str, password: str):
        self.base_url = base_url

        self.login = login
        self.password = password

        self.session = requests.Session()

    def _request(self, method, location=None, full_url=None, params=None, headers=None, data=None, json=None,
                 allow_redirects=False, expected_status=None, jsonify=True):
        if full_url is not None:
            url = full_url
        else:
            url = urljoin(self.base_url, location)

        response = self.session.request(method=method, url=url, params=params, headers=headers, data=data, json=json,
                                        allow_redirects=allow_redirects)

        if expected_status is not None:
            if response.status_code != expected_status:
                raise ResponseStatusCodeException(f'Expected {expected_status}, but got {response.status_code}')

        if jsonify:
            try:
                response_json: dict = response.json()
                if response_json.get('error', None) is not None:
                    error = response_json['error'].get('code', 'UNKNOWN_ERROR')
                    error_message = response_json['error'].get('message', 'This is unknown error.')
                    raise ResponseErrorException(f'Request {url} return error "{error}" with message "{error_message}"')
                return response_json
            except:
                raise ResponseJsonParseError('Response body does not contain valid json')

        return response

    def params_to_string(self, params: dict):
        params_string = "&".join("%s=%s" % (k, v) for k, v in params.items())
        return params_string

    def get_auth(self):

        url = 'https://auth-ac.my.com/auth'

        params = {
            'lang': 'ru',
            'nosavelogin': 0
        }

        data = {
            'email': self.login,
            'password': self.password,
            'continue': 'https://target-sandbox.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email',
            'failure': 'https://account.my.com/login/'
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://target-sandbox.my.com',
            'Referer': 'https://target-sandbox.my.com/'
        }

        response = self._request(method='POST', full_url=url, params=params, headers=headers, data=data,
                                 allow_redirects=True, jsonify=False)


        return self.session.cookies

    def get_csrf(self):
        location = 'csrf/'
        cookie = self.get_auth()

        response = self._request(method='GET', location=location, jsonify=False, allow_redirects=True)
        self.set_x_csrf_header()
        return response

    def set_x_csrf_header(self):
        x_csrf = self.session.cookies.get_dict()['csrftoken']
        x_csrf_header = {'X-CSRFToken': f'{x_csrf}'}
        self.session.headers.update(x_csrf_header)
        return x_csrf_header

    # Segments request start

    def get_vk_groups(self, full_url):
        location = 'api/v2/vk_groups.json'

        params = {
            '_q': full_url
        }

        response = self._request(method='GET', location=location, params=params)

        return response

    def post_vk_group_add(self, vk_group_id):
        location = 'api/v2/remarketing/vk_groups/bulk.json'

        params_dict = {
            'fields': 'id,object_id,name,users_count,url'
        }
        params = self.params_to_string(params_dict)

        json = {
            'items': [
                {
                    'object_id': vk_group_id
                }
            ]
        }

        response = self._request(method='POST', location=location, params=params, json=json)

        return response

    def get_bulk_vk_groups(self):
        pass

    def post_segments_add(self, name, relations):
        location = 'api/v2/remarketing/segments.json'

        params_dict = {
            'fields': 'relations__object_type,relations__object_id,relations__params,'
                      'relations__params__score,relations__id,relations_count,id,name,pass_condition,'
                      'created,campaign_ids,users,flags'
        }
        params = self.params_to_string(params_dict)

        headers = {
            'Content-Type': 'application/json'
        }

        json = {
            "name": name,
            "pass_condition": 1,
            "relations": relations,
            "logicType": "rule"
        }

        response = self._request(method='POST', location=location, params=params, headers=headers, json=json)

        return response

    def delete_segment(self, segment_id):
        location = f'api/v2/remarketing/segments/{segment_id}.json'
        response = self._request(method='DELETE', location=location, expected_status=204)

        return response

    # Campaigns requests start

    def get_campaign_media(self):
        pass