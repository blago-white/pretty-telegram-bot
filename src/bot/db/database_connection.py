import time
import psycopg2

from src.bot.simple import dataclass
from src.bot.simple.jsons import json_getters

from src.conf import dbconfig


class PostgreConnection:
    _TIME_START_SESSION: int

    CONNECTION: psycopg2.connect = None
    NAMEDB: str

    def __init__(self, nameDB: str, user: str, password: str) -> None:

        """
        :param nameDB: str, name of you database
        :param user: str, name user postgres
        :param password: str, posttgres password
        """

        self._TIME_START_SESSION = 0
        self.NAMEDB = nameDB

        self._start_connection(dbname=nameDB, password=password, user=user)

    def _act_time_before_start(self, rounded: int = 8):
        if self._TIME_START_SESSION:
            return round((time.time() - self._TIME_START_SESSION), rounded)

    def _start_connection(self, dbname: str, password: str, user: str):
        if not self.CONNECTION:
            try:
                self.CONNECTION = psycopg2.connect(dbname=dbname,
                                                   user=user,
                                                   password=password)

            except Exception as exception:
                raise exception

            self._TIME_START_SESSION = time.time()

            print('Connection successful! ~~~~~~~~~~~')

    def exit(self):
        if self.CONNECTION:
            try:
                self.CONNECTION.close()

            except:
                print('ERROR EXITING!')

            working_time = self._act_time_before_start(rounded=2)

            d = working_time // 86400
            h = (working_time - d * 86400) // 3600
            m = (working_time - (d * 86400 + h * 3600)) // 60
            s = working_time % 60

            print(f'Time session: {int(d)}d. {int(h)}h. {int(m)}m. {s}sec.')
            print('Bye! ~~~~~~~~~~~')
