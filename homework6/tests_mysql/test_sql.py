import pytest

from models.biggest_requests_by_size import BiggestReqModel
from models.req_by_method import ReqByMethodModel
from models.top_ips_500 import TopIpsModel
from models.top_ten_requests import TopTenReqModel
from models.total_req import TotalReqModel
from mysql.client import MysqlClient
from utils.builder import MysqlBuilder

from utils.logs_analyze import LogAnalyzer


class MyTest:
    def prepare(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client, files_path):
        self.client: MysqlClient = mysql_client
        self.builder: MysqlBuilder = MysqlBuilder(self.client, files_path)
        self.prepare()

    def get_table_data(self, table_model, **filters):
        self.client.session.commit()
        return self.client.session.query(table_model).filter_by(**filters).all()


class TestTotalLogReq(MyTest):
    def prepare(self):
        self.builder.create_total_req()

    def test_total_req(self):
        total_req = self.get_table_data(table_model=TotalReqModel)
        total_req_analyzer = self.builder.log_analyzer.get_total_requests()

        assert len(total_req) == 1
        assert total_req[0].file_name == self.builder.log_file_name
        assert total_req[0].total_req == total_req_analyzer


class TestReqByMethod(MyTest):

    def prepare(self):
        self.builder.create_req_by_method()

    def test_req_by_method(self):
        req_by_method = self.get_table_data(table_model=ReqByMethodModel)
        req_by_method_analyzer = self.builder.log_analyzer.get_total_requests_by_method()

        assert len(req_by_method) == len(req_by_method_analyzer)
        assert req_by_method[0].request_method == req_by_method_analyzer[0][0]
        assert req_by_method[0].total_req == req_by_method_analyzer[0][1]


class TestTopTenRequests(MyTest):

    def prepare(self):
        self.builder.create_top_ten_requests()

    def test_top_ten_requests(self):
        top_ten_req = self.get_table_data(table_model=TopTenReqModel)
        top_ten_req_analyzer = self.builder.log_analyzer.get_top_requests()

        assert len(top_ten_req) == len(top_ten_req_analyzer)
        assert top_ten_req[0].request_url == top_ten_req_analyzer[0][1]
        assert top_ten_req[0].total_req == top_ten_req_analyzer[0][0]


class TestBiggestReq(MyTest):

    def prepare(self):
        self.builder.create_biggest_req()

    def test_biggest_req(self):
        biggest_req = self.get_table_data(table_model=BiggestReqModel)
        biggest_req_analyzer = self.builder.log_analyzer.get_biggest_req_by_size()

        assert len(biggest_req) == len(biggest_req_analyzer)
        assert biggest_req[0].req_url == biggest_req_analyzer[0][2]
        assert biggest_req[0].req_size == biggest_req_analyzer[0][5]
        assert biggest_req[0].req_code == int(biggest_req_analyzer[0][4])
        assert biggest_req[0].ip == biggest_req_analyzer[0][0]


class TestTopIps500(MyTest):

    def prepare(self):
        self.builder.create_top_ips_500()

    def test_top_ips_500(self):
        top_ips_500 = self.get_table_data(table_model=TopIpsModel)
        top_ips_500_analyzer = self.builder.log_analyzer.get_most_often_ip_500()

        assert len(top_ips_500) == len(top_ips_500_analyzer)
        assert top_ips_500[0].total_req == top_ips_500_analyzer[0][0]
        assert top_ips_500[0].ip == top_ips_500_analyzer[0][1]
