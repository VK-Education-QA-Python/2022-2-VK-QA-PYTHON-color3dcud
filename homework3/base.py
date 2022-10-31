import pytest
#from api.builder import Builder


class ApiBase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client):
        self.api_client = api_client
        # self.builder = Builder()  -- TODO: Понять, нужен ли билдер и для чего

        if self.authorize:
            self.api_client.get_csrf()