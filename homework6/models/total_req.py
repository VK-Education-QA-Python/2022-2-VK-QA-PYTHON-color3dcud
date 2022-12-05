from sqlalchemy import Column, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base

TotalReqBase = declarative_base()


class TotalReqModel(TotalReqBase):
    __tablename__ = 'total_req'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'Filename = {self.file_name}, total_requests = {self.total_req}'

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(CHAR(50), nullable=False)
    total_req = Column(Integer, nullable=False)
