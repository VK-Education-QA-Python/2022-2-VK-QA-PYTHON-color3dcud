from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR

TopIpsBase = declarative_base()


class TopIpsModel(TopIpsBase):

    __tablename__ = 'top_ips_500'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'Ip ={self.ip}, total requests = {self.total_req}'

    ip = Column(VARCHAR(30), primary_key=True, unique=True)
    total_req = Column(Integer, nullable=False)
