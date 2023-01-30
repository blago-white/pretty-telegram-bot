import time
import psycopg2

from src.bot.bin import dataclass
from src.bot.bin.jsons import json_writers, json_getters


class Connections:
    __TIME_START_SESSION: int

    CONNECTION: psycopg2.connect = None
    NAMEDB: str

    USER_DATA_TABLES: list[str]
    OTHER_TABLES: list[str]
    TABLES: list[str]

    def __init__(self, NameDB: str, **kwargs) -> None:

        """

        :param NameDB: str, name of you database
        :param kwargs:
        password: str, posttgres password |
        user: str, name user postgres |
        debug: bool, debug mode |

        """

        self.__TIME_START_SESSION = 0
        self.NAMEDB = NameDB

        if not kwargs:
            raise ValueError('Enter password and user')

        if 'password' not in kwargs or 'user' not in kwargs:
            raise ValueError('Not correct data in password or user')

        if 'debug' not in kwargs:
            self.DEBUG = True

        else:
            self.DEBUG = bool(kwargs['debug'])

        self.start_server(password=kwargs['password'],
                          user=kwargs['user'])

        data = json_getters.get_tables().object

        self.USER_DATA_TABLES = data['data']['user_data_tables']
        self.OTHER_TABLES = data['data']['other_tables']
        self.TABLES = data['data']['tables']

        if json_getters.get_condition('restart').object:
            self.delete_data_from_db()

            json_writers.write_condition(cond=False)

    def __act_time_before_start(self, rounded: int = 8):
        if self.__TIME_START_SESSION:
            return round((time.time() - self.__TIME_START_SESSION), rounded)

    def start_server(self, password: str, user: str):
        if not self.CONNECTION:
            try:
                self.CONNECTION = psycopg2.connect(dbname=self.NAMEDB,
                                                   user=user,
                                                   password=password)

                self.__TIME_START_SESSION = time.time()

            except Exception as e:
                return RuntimeError(e)

            print('Connection successful! ~~~~~~~~~~~')

    def execute_query_(self, sqlquery: str) -> dataclass.ResultOperation:

        if self.CONNECTION:
            return execute_query(connection=self.CONNECTION, sqlquery=sqlquery)

    def exit(self):
        if self.CONNECTION:
            if self.DEBUG:
                self.delete_data_from_db()

            self.CONNECTION.close()

            TimeOut = self.__act_time_before_start(rounded=2)

            d = TimeOut // 86400
            h = (TimeOut - d * 86400) // 3600
            m = (TimeOut - (d * 86400 + h * 3600)) // 60
            s = TimeOut % 60

            print(f'Time session: {int(d)}d. {int(h)}h. {int(m)}m. {s}sec.')
            print('Bye! ~~~~~~~~~~~')

    def delete_data_from_db(self) -> dataclass.ResultOperation:
        with self.CONNECTION.cursor() as cursor:

            sql = str()

            for table in self.TABLES:
                sql += 'DELETE FROM %s;' % table

            try:
                cursor.execute(sql)

            except:
                json_writers.write_condition(cond=True)
                return dataclass.ResultOperation(status=False, description='error with deleting from _db_scripts')

        self.CONNECTION.commit()


def execute_query(
        connection: psycopg2.connect,
        sqlquery: str):
    with connection.cursor() as con:

        con.execute(sqlquery)

        # except:
        #     return dataclass.ResultOperation(status=False, description='Error with executing')

        try:
            data = con.fetchall()
            return dataclass.ResultOperation(object=data)

        except:
            connection.commit()
            return dataclass.ResultOperation()
