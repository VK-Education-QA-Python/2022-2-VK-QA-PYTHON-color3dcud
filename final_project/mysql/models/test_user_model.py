from sqlalchemy import Column, INTEGER, VARCHAR, SMALLINT, DATETIME
from sqlalchemy.ext.declarative import declarative_base

TestUserBase = declarative_base()


class TestUserModel(TestUserBase):
    __tablename__ = 'test_users'
    __table_args__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'id = "{self.id}",\n' \
               f'name = "{self.name}",\n' \
               f'surname = "{self.surname}",\n' \
               f'middle_name = "{self.middle_name}",\n' \
               f'username = "{self.username}",\n' \
               f'password = "{self.password}",\n' \
               f'email = "{self.email}",\n' \
               f'access = "{self.access}",\n' \
               f'active = "{self.active}",\n' \
               f'start_active_time = "{self.start_active_time}"'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), default=None)
    surname = Column(VARCHAR(255), default=None)
    middle_name = Column(VARCHAR(255), default=None)
    username = Column(VARCHAR(16), default=None, unique=True)
    password = Column(VARCHAR(255), default=None)
    email = Column(VARCHAR(64), default=None, unique=True)
    access = Column(SMALLINT, default=None)
    active = Column(SMALLINT, default=None)
    start_active_time = Column(DATETIME, default=None)
