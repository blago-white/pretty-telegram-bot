from typing import Union
from psycopg2.extensions import connection
from ._exceptions import SQLSintaxError


class Excecutor:
    def __init__(self, connection_: connection):
        self.postgres_connection = connection_

    def execute_query(self, sqlquery: str) -> Union[tuple, None]:

        """
        :param sqlquery: query to db with SQL
        :return: if successfully - data of fetch (all) or None if operation is not SELECT or the condition did not
        give a result else - baseexception
        """

        with self.postgres_connection.cursor() as connection_:
            try:
                connection_.execute(sqlquery)
            except Exception as exception:
                raise SQLSintaxError(f'POSTGRES ERROR: {str(exception)}')

            try:
                return connection_.fetchall()

            except:
                self.postgres_connection.commit()
