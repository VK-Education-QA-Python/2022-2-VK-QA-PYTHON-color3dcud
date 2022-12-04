from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

TopTenReqBase = declarative_base()


class TopTenReqModel(TopTenReqBase):
    __tablename__ = 'top_ten_requests'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'Request url = {self.request_url}, total requests = {self.total_req}'

    id = Column(Integer, primary_key=True, autoincrement=True)
    request_url = Column(VARCHAR(255), nullable=False)
    total_req = Column(Integer, nullable=False)
