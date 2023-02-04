import time
import psycopg2

from src.bot.simple import dataclass
from src.bot.simple.jsons import json_writers, json_getters
from src.bot.db import postgres_execute

from src.conf import dbconfig


class ConnectionsManagement:
    _TIME_START_SESSION: int

    CONNECTION: psycopg2.connect = None
    NAMEDB: str

    USER_DATA_TABLES = dbconfig.USER_DATA_TABLES
    OTHER_TABLES = dbconfig.OTHER_TABLES
    TABLES = dbconfig.TABLES

    """

    :param NameDB: str, name of you database
    :param kwargs:
    password: str, posttgres password |
    user: str, name user postgres |
    debug: bool, debug mode |

    """

    def __init__(self, NameDB: str, **kwargs) -> None:

        self._TIME_START_SESSION = 0
        self.NAMEDB = NameDB

        if not kwargs:
            raise ValueError('Enter password and user')

        if 'password' not in kwargs or 'user' not in kwargs:
            raise ValueError('Not correct data in password or user')

        if 'debug' not in kwargs:
            self.DEBUG = True

        else:
            self.DEBUG = bool(kwargs['debug'])

        self._start_connection(password=kwargs['password'],
                               user=kwargs['user'])

        if json_getters.get_condition('restart').object:
            self._wipe_database_data()

            json_writers.write_condition(cond=False)

    def _act_time_before_start(self, rounded: int = 8):
        if self._TIME_START_SESSION:
            return round((time.time() - self._TIME_START_SESSION), rounded)

    def _start_connection(self, password: str, user: str):
        if not self.CONNECTION:
            try:
                self.CONNECTION = psycopg2.connect(dbname=self.NAMEDB,
                                                   user=user,
                                                   password=password)

                self._TIME_START_SESSION = time.time()

            except Exception as e:
                return RuntimeError(e)

            print('Connection successful! ~~~~~~~~~~~')

    def execute_query_(self, sqlquery: str) -> dataclass.ResultOperation:
        if self.CONNECTION:
            return dataclass.ResultOperation(object=
                                             postgres_execute.execute_query(
                                                postgres_connection=self.CONNECTION,
                                                sqlquery=sqlquery)
                                             )

    def exit(self):
        if self.CONNECTION:
            if self.DEBUG:
                self._wipe_database_data()

            self.CONNECTION.close()

            working_time = self._act_time_before_start(rounded=2)

            d = working_time // 86400
            h = (working_time - d * 86400) // 3600
            m = (working_time - (d * 86400 + h * 3600)) // 60
            s = working_time % 60

            print(f'Time session: {int(d)}d. {int(h)}h. {int(m)}m. {s}sec.')
            print('Bye! ~~~~~~~~~~~')

    def _wipe_database_data(self) -> dataclass.ResultOperation:
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
