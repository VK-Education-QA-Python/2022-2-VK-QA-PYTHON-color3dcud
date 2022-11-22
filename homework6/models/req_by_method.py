from sqlalchemy import Column, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base

ReqByMethodBase = declarative_base()


class ReqByMethodModel(ReqByMethodBase):
    __tablename__ = 'req_by_method'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'Request method ={self.request_method}, total requests = {self.total_req}'

    request_method = Column(CHAR(20), primary_key=True, unique=True)
    total_req = Column(Integer, nullable=False)
