import allure
import sqlalchemy
from sqlalchemy.orm import sessionmaker


class MysqlClient:

    def __init__(self, db_name, user, password):
        self.user = user
        self.port = '3306'
        self.password = password
        self.host = '127.0.0.1'
        # self.host = 'project_base'
        self.db_name = db_name

        self.connection = None
        self.engine = None
        self.session = None

    @allure.step('Подключаемся к БД')
    def connect(self, db_created=True):
        db = self.db_name if db_created else ''
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'
        self.engine = sqlalchemy.create_engine(url)
        self.connection = self.engine.connect()

        session = sessionmaker(bind=self.connection.engine)
        self.session = session()

    @allure.step('Поиск данных в БД')
    def get_table_data(self, table_model, **filters):
        self.session.commit()
        return self.session.query(table_model).filter_by(**filters).first()

    @allure.step('Получение всех данных из БД')
    def get_all_table_data(self, table_model, **filters):
        self.session.commit()
        return self.session.query(table_model).filter_by(**filters).all()
