from typing import Union


class Excecutor:

    def __init__(self, connection):
        self.postgres_connection = connection

    def execute_query(self, sqlquery: str) -> Union[tuple, None]:

        """
        :param sqlquery: query to db with SQL
        :return: if successfully - data of fetch (all) or None if operation is not SELECT or the condition did not
        give a result else - baseexception
        """

        with self.postgres_connection.cursor() as connection:
            try:
                connection.execute(sqlquery)

            except Exception as exception:
                print(exception)
                return BaseException(str(exception))

            try:
                return connection.fetchall()

            except:
                self.postgres_connection.commit()
