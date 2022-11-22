import pytest

from models.biggest_requests_by_size import BiggestReqModel
from models.req_by_method import ReqByMethodModel
from models.top_ips_500 import TopIpsModel
from models.top_ten_requests import TopTenReqModel
from models.total_req import TotalReqModel
from mysql.client import MysqlClient
from utils.builder import MysqlBuilder


class MyTest:

    def prepare(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client, files_path):
        self.client: MysqlClient = mysql_client
        self.builder: MysqlBuilder = MysqlBuilder(self.client, files_path)
        self.prepare()

    def get_total_req(self, **filters):
        self.client.session.commit()
        return self.client.session.query(TotalReqModel).filter_by(**filters).all()

    def get_req_by_method(self, **filters):
        self.client.session.commit()
        return self.client.session.query(ReqByMethodModel).filter_by(**filters).all()

    def get_top_ten_requests(self, **filters):
        self.client.session.commit()
        return self.client.session.query(TopTenReqModel).filter_by(**filters).all()

    def get_biggest_req(self, **filters):
        self.client.session.commit()
        return self.client.session.query(BiggestReqModel).filter_by(**filters).all()

    def get_top_ips_500(self, **filters):
        self.client.session.commit()
        return self.client.session.query(TopIpsModel).filter_by(**filters).all()


class TestTotalLogReq(MyTest):
    LOG_NAME = 'access.log'

    def prepare(self):
        self.builder.create_total_req()

    def test_total_req(self):
        total_req = self.get_total_req()

        assert len(total_req) == 1
        assert total_req[0].file_name == 'access.log'


class TestReqByMethod(MyTest):

    def prepare(self):
        self.builder.create_req_by_method()

    def test_req_by_method_len(self):
        req_by_method = self.get_req_by_method()

        assert len(req_by_method) == 4


class TestTopTenRequests(MyTest):

    def prepare(self):
        self.builder.create_top_ten_requests()

    def test_top_ten_requests_len(self):
        top_ten_req = self.get_top_ten_requests()

        assert len(top_ten_req) == 10


class TestBiggestReq(MyTest):

    def prepare(self):
        self.builder.create_biggest_req()

    def test_biggest_req_len(self):
        biggest_req = self.get_biggest_req()

        assert len(biggest_req) == 5
        assert biggest_req[-1].req_size == 1417


class TestTopIps500(MyTest):

    def prepare(self):
        self.builder.create_top_ips_500()

    def test_top_ips_500_len(self):
        top_ips_500 = self.get_top_ips_500()

        assert len(top_ips_500) == 5
        assert top_ips_500[0].total_req == 225
        assert top_ips_500[0].ip == '189.217.45.73'
