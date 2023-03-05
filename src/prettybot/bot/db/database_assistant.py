import datetime

import psycopg2.extras
from typing import Union

from src.prettybot.scripts import json_getters
from src.prettybot.dataclass import dataclass
from src.prettybot.db import sql_placeholder
from src.prettybot.db import sql_query_executor
from src.prettybot.db import database_connection

from src.conf.dbconfig import *
from src.conf.recording_stages import *


class UserConditions:
    ...


class UserData:
    ...


class UserMessages:
    ...


class DBGetter:
    _executor: sql_query_executor.Excecutor

    def get_logging_info(self, user_id: int) -> dataclass.ResultOperation:
        response = self._executor.execute_query(sql_placeholder.fill_sql_template(user_id, number_temp=1))

        if type(response) is BaseException:
            return dataclass.ResultOperation(False, 'database error')

        if not len(response):
            return dataclass.ResultOperation(description='not info')

        return dataclass.ResultOperation(object=response[0])

    def get_chatting_condition(self, user_id: int) -> Union[bool, BaseException]:

        """
        :param user_id: bot id of current user
        :return: condition of chatting user or baseexception
        """

        data = self._executor.execute_query(
            sql_placeholder.fill_sql_template(user_id, number_temp=23)
        )

        return dataclass.ResultOperation(status=False if type(data) is BaseException else True,
                                         object=data if type(data) is BaseException else data[0][0])

    def get_main_message(self, user_id: int, type_message: int):
        if not (user_id or type_message):
            return dataclass.ResultOperation(status=False, description='not full args')

        id_msg = self._executor.execute_query(
            sql_placeholder.fill_sql_template(user_id, type_message, number_temp=16))

        if type(id_msg) is BaseException:
            return dataclass.ResultOperation(status=False, object=id_msg)

        if not id_msg:
            return dataclass.ResultOperation(status=True, description='mes not found')

        return dataclass.ResultOperation(object=int(id_msg[0][0]))

    def _get_cities(self) -> dataclass.ResultOperation:
        result = {}
        response = self._executor.execute_query(sql_placeholder.fill_sql_template(number_temp=17))

        if type(response) is BaseException:
            return dataclass.ResultOperation(status=False, description='database error')

        for city in response:
            region = city[1]
            region = region.replace('область',
                                    'обл.').replace('Республика',
                                                    'Респ.').replace('автономный округ',
                                                                     'a.о.').replace('автономная область',
                                                                                     'a.обл.')

            result.update({str.lower(city[0]): f'<b>{city[0]}</b> [{region}]'})

        return dataclass.ResultOperation(object=result)

    def get_user_lang_code(self, user_id: int) -> str:
        lang_response = self.get_user_data_by_table(user_id=user_id, table_name='users')
        print(lang_response)
        if lang_response.status and lang_response.object:
            if lang_response.object[-1][-1]:
                return lang_response.object[-1][-1]

        return DEFAULT_LANG

    def get_user_data_by_table(self, user_id: int, table_name: str) -> dataclass.ResultOperation:
        result = self._executor.execute_query(sql_placeholder.fill_sql_template(table_name, user_id, number_temp=19))

        return dataclass.ResultOperation(
            status=True if type(result) is not BaseException else False,
            object=result
        )

    def get_user_entrys(self, user_id: int):
        if self.get_user_data_by_table(user_id=user_id, table_name='users') is not BaseException:

            results = [self.get_user_data_by_table(user_id=user_id, table_name=name) for name in
                       USER_DATA_TABLES]

            for r in results:
                if type(r) is BaseException:
                    return dataclass.ResultOperation(status=False, description='database error')

            results = [result.object for result in results]

            for idx, dbdata in enumerate(results):
                if type(dbdata) is not BaseException and len(dbdata):
                    results[idx] = results[idx][0]

            result = {}
            for idx, table_name in enumerate(USER_DATA_TABLES):
                result.update({table_name: results[idx]})

            return dataclass.ResultOperation(object=result, description='ann have')

        else:
            return dataclass.ResultOperation('not ann')

    def get_users_ids_by_params(
            self,
            user_id: int,
            age_range: psycopg2.extras.NumericRange = None,
            city: str = None,
            sex: bool = None):

        if age_range and city and sex and user_id:
            result = self._executor.execute_query(sql_placeholder.fill_sql_template(
                age_range, city, sex, user_id, number_temp=18
            ))

        else:
            result = self._executor.execute_query(sql_placeholder.fill_sql_template(user_id, number_temp=25))

        return dataclass.ResultOperation(
            status=True if type(result) is not BaseException else False,
            object=result[0][0]
        )

    def get_user_buffer_status(self, user_id: int):

        from_bufer_data = self._executor.execute_query(sqlquery=sql_placeholder.fill_sql_template(
            'users_searching_buffer',
            user_id,
            number_temp=19))

        return dataclass.ResultOperation(
            status=True,
            object=True if from_bufer_data else False)

    def get_user_wishes(self, user_id: int) -> dataclass.ResultOperation:
        result = self._executor.execute_query(sql_placeholder.fill_sql_template(user_id, number_temp=2))[0]
        return dataclass.ResultOperation(
            status=True if type(result) is not BaseException else False,
            object=result
        )


class DBSetter:
    _executor: sql_query_executor.Excecutor

    def change_state_logging(self, user_id: int, logtype=None, logstage=None, stop_logging: bool = None):
        if stop_logging:
            response = self._executor.execute_query(sql_placeholder.fill_sql_template(user_id, number_temp=3))
            if type(response) is BaseException:
                return dataclass.ResultOperation(status=False, description='_postgre_conn error 1')

            return dataclass.ResultOperation()

        if logtype == TYPE_RECORDING[1]:
            response = self._executor.execute_query(sql_placeholder.fill_sql_template(logtype, logstage, user_id,
                                                                                      number_temp=4))

            if type(response) is BaseException:
                return dataclass.ResultOperation(False, '_postgre_conn error 2')

            return dataclass.ResultOperation()

        response = self._executor.execute_query(sql_placeholder.fill_sql_template(logtype, logstage, user_id,
                                                                                  number_temp=4))
        if type(response) is BaseException:
            dataclass.ResultOperation(status=False, description='_postgre_conn error 3')

        return dataclass.ResultOperation()

    def change_chatting_condition(self, user_id: int, new_condition: bool) -> None:
        self._executor.execute_query(
            sql_placeholder.fill_sql_template(bool(new_condition), int(user_id), number_temp=24)
        )

    def change_user_lang(self, user_id: int, lang_code: str):
        self._executor.execute_query(sql_placeholder.fill_sql_template(lang_code, user_id, number_temp=21))

    def save_photo(self, user_id: int, file_id, upd=False):
        if not upd:
            response = self._executor.execute_query(
                sql_placeholder.fill_sql_template(user_id, file_id, number_temp=5))

        else:
            response = self._executor.execute_query(
                sql_placeholder.fill_sql_template(file_id, user_id, number_temp=6))

        return dataclass.ResultOperation(object=response)

    def add_main_message_to_db(self, user_id: int, id_message: int, type_message: int):

        if not (user_id or id_message or type_message) or type_message not in TYPES_MAIN_MESSAGES:
            return dataclass.ResultOperation(status=False, description='args')

        existing_message = super().get_main_message()

        self._executor.execute_query(sql_placeholder.fill_sql_template(user_id,
                                                                       id_message,
                                                                       int(type_message),
                                                                       number_temp=14))

        return dataclass.ResultOperation()

    def record_user_param(self, user_id: int, name: str, value: Union[str, int, bool]):
        print(name, value, '-----f')
        try:
            response = self._executor.execute_query(
                sqlquery=sql_placeholder.fill_sql_template(name, value, user_id, number_temp=10)
            )

            return dataclass.ResultOperation(
                status=True if type(response) is not BaseException else False
            )

        except TypeError:
            return dataclass.ResultOperation(status=False,
                                             description='Not correct datatype')

    def del_user_annotations(self, user_id):
        for dbname in TABLES:
            self._executor.execute_query(sql_placeholder.fill_sql_template(dbname, user_id, number_temp=20))

    def add_user_entry(self, user_id, fname, lname, telegname, date_message):
        try:
            response1 = self._executor.execute_query(sql_placeholder.fill_sql_template(user_id,
                                                                                       fname,
                                                                                       lname,
                                                                                       telegname,
                                                                                       date_message,
                                                                                       number_temp=7))

            response2 = self._executor.execute_query(sql_placeholder.fill_sql_template(user_id,
                                                                                       True,
                                                                                       DEFAULT_LOGGING_TYPE,
                                                                                       DEFAULT_LOGGING_STAGE,
                                                                                       False,
                                                                                       number_temp=8))

            response3 = self._executor.execute_query(sql_placeholder.fill_sql_template(user_id, number_temp=9))

        except KeyError:
            return dataclass.ResultOperation(status=False, description='not all user_data')

        if BaseException in (response1, response2, response3):
            return dataclasses.ResultOperation(status=False, description='DB error')

        return dataclass.ResultOperation()

    def del_main_message_from_db(self, user_id, type_message):
        if not (user_id or type_message):
            return dataclass.ResultOperation(status=False, description='not full args')

        response = self._executor.execute_query(
            sql_placeholder.fill_sql_template(user_id, type_message, number_temp=15)
        )

        if type(response) is BaseException:
            return dataclass.ResultOperation(status=False, description='deleting error')

        return dataclass.ResultOperation()

    def del_user_from_buffer(self, user_id: int):
        self._executor.execute_query(
            sqlquery=sql_placeholder.fill_sql_template(user_id, number_temp=26)
        )

    def add_user_to_buffer(self, user_id: int, date_message: datetime.datetime, specified_search: bool):
        self._executor.execute_query(
            sqlquery=sql_placeholder.fill_sql_template(
                user_id,
                date_message,
                specified_search,
                number_temp=27)
        )


class DatabaseScripts(DBGetter, DBSetter):
    all_cities: dict[str]
    _executor: sql_query_executor.Excecutor
    _postgre_conn: database_connection

    def __init__(self):
        db_settings = json_getters.get_setings_db()

        if not db_settings.status:
            raise RuntimeError('json getting error')

        self._postgre_conn = database_connection.PostgreConnection(nameDB=db_settings.object['namedb'],
                                                                   password=db_settings.object['password'],
                                                                   user=db_settings.object['user'])

        self._executor = sql_query_executor.Excecutor(connection=self._postgre_conn.CONNECTION)

        if not self._executor or not self._postgre_conn:
            raise ConnectionError('error with initializing database')

        self.all_cities = self._get_cities()

        if not self.all_cities.status:
            raise RuntimeError('error with database (_get_cities)')

        self.all_cities = self.all_cities.object

    def stop(self) -> None:
        if self._postgre_conn:
            self._postgre_conn.exit()
