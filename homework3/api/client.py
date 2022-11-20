from urllib.parse import urljoin

import requests

from api.custom_api_exceptions import *
from static.api_urls import *
from static.requests_body import *


class ApiClient:
    COOKIES_LIST = ['mc', 'sdc', 'z', 'csrftoken']

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

        url = AUTH
        params = GET_AUTH_PARAMS
        data = get_auth_body(login=self.login, password=self.password)
        headers = GET_AUTH_HEADERS

        response = self._request(method='POST', full_url=url, params=params, headers=headers, data=data,
                                 allow_redirects=True, jsonify=False)

        return response

    def get_csrf(self):
        location = CSRF_LOCATION
        self.get_auth()

        response = self._request(method='GET', location=location, jsonify=False, allow_redirects=True)
        self.set_x_csrf_header()
        self.check_cookies()

        return response

    def set_x_csrf_header(self):
        x_csrf = self.session.cookies.get_dict()['csrftoken']
        x_csrf_header = {'X-CSRFToken': f'{x_csrf}'}
        self.session.headers.update(x_csrf_header)
        return x_csrf_header

    def check_cookies(self):
        cookies = self.session.cookies.get_dict()

        for cookie in self.COOKIES_LIST:
            try:
                cookies[cookie]
            except:
                raise MissingAuthorizationCookie(f'Authorization cookie - {cookie} - is missing')

    # Segments request start

    def get_vk_groups(self, full_url):
        location = GET_VK_GROUPS_LOCATION
        params = get_vk_groups_params(full_url=full_url)
        response = self._request(method='GET', location=location, params=params)

        return response

    def post_vk_group_add(self, vk_group_id):
        location = POST_VK_GROUP_ADD_LOCATION
        params_dict = POST_VK_GROUP_ADD_PARAMS
        params = self.params_to_string(params_dict)
        json = post_vk_group_add_body(vk_group_id=vk_group_id)

        response = self._request(method='POST', location=location, params=params, json=json)

        return response

    def delete_vk_group(self, vk_group_id):
        location = delete_vk_group_location(vk_group_id=vk_group_id)

        response = self._request(method='DELETE', location=location, expected_status=204, jsonify=False)

        return response

    def get_your_vk_groups(self):
        location = GET_YOUR_VK_GROUPS_LOCATION
        params = GET_YOUR_VK_GROUPS_PARAMS

        response = self._request(method='GET', location=location, params=params, expected_status=200)

        return response

    def post_segments_add(self, name, relations):
        location = POST_SEGMENT_ADD_LOCATION

        params_dict = POST_SEGMENTS_ADD_PARAMS
        params = self.params_to_string(params_dict)
        headers = POST_SEGMENTS_ADD_HEADERS
        json = post_segments_add_body(name=name, relations=relations)

        response = self._request(method='POST', location=location, params=params, headers=headers, json=json)

        return response

    def delete_segment(self, segment_id):
        location = delete_segment_location(segment_id=segment_id)
        response = self._request(method='DELETE', location=location, expected_status=204, jsonify=False)

        return response

    def get_segments_list(self):
        location = GET_SEGMENTS_LIST_LOCATION
        params_dict = GET_SEGMENTS_LIST_PARAMS
        params = self.params_to_string(params=params_dict)

        response = self._request(method='GET', location=location, params=params)

        return response
