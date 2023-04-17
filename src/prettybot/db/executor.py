from typing import Union

import psycopg2.extensions
from psycopg2 import extensions

from . import _exceptions

__all__ = ['Excecutor']


class Excecutor:
    def __init__(self, postgre_connection: extensions.connection):
        self._postgres_connection = postgre_connection

    def execute_query(self, sqlquery: str) -> Union[tuple, None]:

        """
        :param sqlquery: query to db with SQL
        :return: if successfully - data of fetch (all) or None if operation is not SELECT or the condition did not
        give a result else - baseexception
        """
        with self._postgres_connection.cursor() as connection_:
            try:
                connection_.execute(sqlquery)
            except Exception as exception:
                raise _exceptions.SQLSintaxError(f'POSTGRES ERROR: {str(exception)}')

            try:
                return connection_.fetchall()

            except:
                self._postgres_connection.commit()
