from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, CHAR

TotalReqBase = declarative_base()


class TotalReqModel(TotalReqBase):

    __tablename__ = 'total_req'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'Filename ={self.file_name}, total_requests = {self.total_req}'

    file_name = Column(CHAR(50), primary_key=True)
    total_req = Column(Integer, nullable=False)
