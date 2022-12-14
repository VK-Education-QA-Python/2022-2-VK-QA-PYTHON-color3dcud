from urllib.parse import urljoin

import allure
import requests

from api.api_exceptions import (ResponseErrorException, ResponseJsonParseError,
                                MissingAuthorizationCookie)
from static.api.api_locations import *
from static.credentials import CREDENTIALS


class ApiClient:
    AUTHORIZATION_COOKIES = ['session']

    @allure.step('Инициализация ApiClient')
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.session = requests.Session()

    def _request(self, method, location, params=None, headers=None, data=None, json=None, allow_redirects=False,
                 jsonify=False):

        url = urljoin(self.base_url, location)

        response = self.session.request(method=method, url=url, params=params, headers=headers, data=data, json=json,
                                        allow_redirects=allow_redirects)

        if jsonify:
            try:
                response_json: dict = response.json()
                if response_json.get('status', ) == 'failed':
                    error = response_json['error'].get('code', 'UNKNOWN_ERROR')
                    error_message = response_json['error'].get('message', 'This is unknown error.')
                    raise ResponseErrorException(f'Request {url} return error "{error}" with message "{error_message}"')
                return response_json
            except:
                raise ResponseJsonParseError('Response body does not contain valid json')

        return response

    @allure.step('Авторизация пользователя')
    def authorization(self, username=CREDENTIALS['main']['username'], password=CREDENTIALS['main']['password'],
                      check_cookies=True):
        location = AUTHORIZATION_LOCATION

        data = {
            'username': username or self.username,
            'password': password or self.password,
            'submit': 'Login'
        }

        response = self._request(method='POST', location=location, data=data, allow_redirects=False,
                                 jsonify=False)

        if check_cookies:
            cookies = self.session.cookies.get_dict()
            for cookie in self.AUTHORIZATION_COOKIES:
                try:
                    cookies[cookie]
                except:
                    raise MissingAuthorizationCookie(f'Authorization cookie - {cookie} - is missing')

        return response

    @allure.step('Логаут')
    def get_logout(self):
        location = LOGOUT_LOCATION
        response = self._request(method='GET', location=location)

        return response

    @allure.step('Добавление пользователя')
    def post_create_user(self, new_user: dict):
        location = POST_CREATE_USER_LOCATION
        json = new_user
        response = self._request(method='POST', location=location, json=json)

        return response

    @allure.step('Удаление пользователя')
    def delete_user(self, username):
        location = DELETE_USER_LOCATION.format(username=username)
        response = self._request(method='DELETE', location=location, jsonify=False)

        return response

    @allure.step('Смена пароля пользователя')
    def put_change_password(self, username, new_password):
        location = PUT_CHANGE_PASSPORT_LOCATION.format(username=username)
        json = {
            'password': new_password
        }
        response = self._request(method='PUT', location=location, json=json, jsonify=False)

        return response

    @allure.step('Блокировка пользователя')
    def post_block_user(self, username):
        location = POST_BLOCK_USER_LOCATION.format(username=username)
        response = self._request(method='POST', location=location)

        return response

    @allure.step('Разблокировка пользователя')
    def post_accept_user(self, username):
        location = POST_ACCEPT_USER_LOCATION.format(username=username)
        response = self._request(method='POST', location=location)

        return response

    @allure.step('Получение статуса приложения')
    def get_status(self):
        location = GET_STATUS_LOCATION
        response = self._request(method='GET', location=location)

        return response
