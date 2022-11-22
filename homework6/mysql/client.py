import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models.total_req import TotalReqBase as BaseReq
from models.req_by_method import ReqByMethodBase
from models.top_ten_requests import TopTenReqBase
from models.biggest_requests_by_size import BiggestReqBase
from models.top_ips_500 import TopIpsBase


class MysqlClient:

    def __init__(self, db_name, user, password):
        self.user = user
        self.port = '3306'
        self.password = password
        self.host = '127.0.0.1'
        self.db_name = db_name

        self.connection = None
        self.engine = None
        self.session = None

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'
        self.engine = sqlalchemy.create_engine(url)
        self.connection = self.engine.connect()

        session = sessionmaker(bind=self.connection.engine)
        self.session = session()

    def create_db(self):
        self.connect(db_created=False)
        self.execute_query(f'DROP database IF EXISTS {self.db_name}')
        self.execute_query(f'CREATE database {self.db_name}')

    def execute_query(self, query, fetch=False):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

    def create_table_total_requests(self):
        if not sqlalchemy.inspect(self.engine).has_table('total_req'):
            BaseReq.metadata.tables['total_req'].create(self.engine)

    def create_table_req_by_method(self):
        if not sqlalchemy.inspect(self.engine).has_table('req_by_method'):
            ReqByMethodBase.metadata.tables['req_by_method'].create(self.engine)

    def create_table_top_ten_requests(self):
        if not sqlalchemy.inspect(self.engine).has_table('top_ten_requests'):
            TopTenReqBase.metadata.tables['top_ten_requests'].create(self.engine)

    def create_table_biggest_req(self):
        if not sqlalchemy.inspect(self.engine).has_table('biggest_req'):
            BiggestReqBase.metadata.tables['biggest_req'].create(self.engine)

    def create_table_top_ips_500(self):
        if not sqlalchemy.inspect(self.engine).has_table('top_ips_500'):
            TopIpsBase.metadata.tables['top_ips_500'].create(self.engine)
