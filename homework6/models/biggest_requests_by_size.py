from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

BiggestReqBase = declarative_base()


class BiggestReqModel(BiggestReqBase):
    __tablename__ = 'biggest_req'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'Request url ={self.req_url}, size = {self.req_size}, code = {self.req_code}, ip = {self.ip}'

    req_url = Column(VARCHAR(512), primary_key=True, )
    req_size = Column(Integer, nullable=False)
    req_code = Column(Integer, nullable=False)
    ip = Column(VARCHAR(30), nullable=False)
