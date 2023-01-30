from typing import Union

from src.bot.bin import dataclass
from src.bot.bin.jsons import json_getters
from src.bot.db import sqlexecutor
from src.etc.config import (LIMIT_REGISTRATION_STAGES,
                            TYPES_MAIN_MESSAGES,
                            DEFAULT_LANG,
                            DEFAULT_LOGGING_TYPE,
                            DEFAULT_LOGGING_STAGE,
                            NAME_COLUMN_BY_LOGSTAGE,
                            WISHES_COLUMNS,
                            LOWER_AGE_LIMIT,
                            UPPER_AGE_LIMIT,
                            DBDEBUG)


class DBGetMethods:
    _database: sqlexecutor.Execute

    def get_logging_info(self, ids: int) -> dataclass.ResultOperation:
        response = self._database.complete_transaction(ids, number_temp=1)

        if not response.status:
            return dataclass.ResultOperation(False, 'database error')

        if not len(response.object):
            return dataclass.ResultOperation(description='not info')

        return dataclass.ResultOperation(object=response.object[0])

    def get_main_message(self, ids: int, type_message: int):
        if not (ids or type_message):
            return dataclass.ResultOperation(status=False, description='not full args')

        id_msg = self._database.complete_transaction(ids, type_message, number_temp=16)

        if not id_msg.object:
            return dataclass.ResultOperation(status=True, description='mes not found')

        return dataclass.ResultOperation(object=int(id_msg.object[0][0]))

    def _get_cities(self):

        result = {}
        response = self._database.complete_transaction('cities', number_temp=17)

        if not response.status:
            return dataclass.ResultOperation(status=False, description='database error')

        for city in response.object:
            region = city[1]
            region = region.replace('область',
                                    'обл.').replace('Республика',
                                                    'Респ.').replace('автономный округ',
                                                                     'a.о.').replace('автономная область',
                                                                                     'a.обл.')

            result.update({str.lower(city[0]): f'<b>{city[0]}</b> [{region}]'})

        return dataclass.ResultOperation(object=result)

    def get_user_lang_code(self, ids: int):
        lang_response = self.get_user_data_by_table(ids=ids, table_name='users')

        if lang_response.object:
            if lang_response.object[-1][-1]:
                return lang_response.object[-1][-1]

        return DEFAULT_LANG

    def get_user_data_by_table(self, ids: int, table_name: str) -> dataclass.ResultOperation:
        return self._database.complete_transaction(table_name, ids, number_temp=19)

    def get_user_entrys(self, ids: int):
        if self.get_user_data_by_table(ids=ids, table_name='users').status:

            results = [self.get_user_data_by_table(ids=ids, table_name=name) for name in
                       self._database.USER_DATA_TABLES]

            for r in results:
                if not r.status:
                    return dataclass.ResultOperation(status=False, description='database error')

            results = [result.object for result in results]

            for idx, dbdata in enumerate(results):
                if len(dbdata):
                    results[idx] = results[idx][0]

            result = {}
            for idx, table_name in enumerate(self._database.USER_DATA_TABLES):
                result.update({table_name: results[idx]})

            return dataclass.ResultOperation(object=result, description='ann have')

        else:
            return dataclass.ResultOperation('not ann')

    def get_user_wishes(self, ids: int) -> dataclass.ResultOperation:
        return self._database.complete_transaction(ids, number_temp=2).object[0]


class DBSetMethods:
    _database: sqlexecutor.Execute

    def change_state_logging(self, ids: int, logtype=None, logstage=None, stop_logging: bool = None):
        if stop_logging:
            response = self._database.complete_transaction(ids, number_temp=3)
            if not response.status:
                return dataclass.ResultOperation(status=False, description='_database error 1')

            return dataclass.ResultOperation()

        if logtype == 2:
            response = self._database.complete_transaction(logtype, logstage, ids, number_temp=4)

            if not response.status:
                return dataclass.ResultOperation(False, '_database error 2')

            return dataclass.ResultOperation()

        if logstage >= LIMIT_REGISTRATION_STAGES:
            response = self._database.complete_transaction(ids, number_temp=3)

        else:
            response = self._database.complete_transaction(logtype, logstage, ids, number_temp=4)

        if not response.status:
            dataclass.ResultOperation(status=False, description='_database error 3')

        return dataclass.ResultOperation()

    def change_user_lang(self, ids: int, lang_code: str):
        self._database.complete_transaction(lang_code, ids, number_temp=21)

    def save_photo(self, ids: int, file_id, upd=False):
        if not upd:
            response = self._database.complete_transaction(ids, file_id, number_temp=5)

        else:
            response = self._database.complete_transaction(file_id, ids, number_temp=6)

        return dataclass.ResultOperation(object=response)

    def add_main_message_to_db(self, ids: int, id_message: int, type_message: int):

        if not (ids or id_message or type_message) or type_message not in TYPES_MAIN_MESSAGES:
            return dataclass.ResultOperation(status=False, description='args')

        self._database.complete_transaction(ids, id_message, int(type_message), number_temp=14)

        return dataclass.ResultOperation()

    def record_user_data_by_stage(self, message_text, ids, logstage, update=False):

        type_err_temp = 'not correct type of %s (need %s) given %s'

        if logstage in NAME_COLUMN_BY_LOGSTAGE:

            processed_text = message_text

            if type(message_text) == str:
                processed_text = message_text.replace("'", "''").replace("/", "")
                processed_text = "'" + processed_text + "'"

            try:
                self._database.complete_transaction(NAME_COLUMN_BY_LOGSTAGE[logstage],
                                                    processed_text,
                                                    ids,
                                                    number_temp=10)

            except TypeError:
                return dataclass.ResultOperation(status=False,
                                                 description=type_err_temp % ('age', int, type(message_text)))

            if logstage in WISHES_COLUMNS:
                if logstage == 1:

                    start_range = int(message_text) - 5
                    stop_range = int(message_text) + 5

                    if start_range < LOWER_AGE_LIMIT:
                        start_range = LOWER_AGE_LIMIT

                    elif stop_range < LOWER_AGE_LIMIT:
                        stop_range = UPPER_AGE_LIMIT

                    self._database.complete_transaction(start_range,
                                                        stop_range,
                                                        ids,
                                                        number_temp=11)

                    return

                if logstage == 2:
                    message_text = "'" + message_text + "'"

                if logstage == 3:
                    message_text = False if message_text else True

                self._database.complete_transaction(NAME_COLUMN_BY_LOGSTAGE[logstage] + '_wish',
                                                    message_text,
                                                    ids,
                                                    number_temp=10)

        elif logstage == 5:

            try:
                response = self.save_photo(ids=ids, file_id=str(message_text), upd=update)

            except TypeError:
                return dataclass.ResultOperation(status=False,
                                                 description=type_err_temp % ('ph_id', str, type(message_text)))

            if not response.status:
                return dataclass.ResultOperation(status=False, description='save photo error 1')

        return dataclass.ResultOperation()

    def del_user_annotations(self, ids):
        for dbname in self._database.TABLES:
            self._database.complete_transaction(dbname, ids, number_temp=20)

    def add_user_entry(self, **user_data):

        if len(user_data) < 8:
            return dataclass.ResultOperation(status=False, description='not all user_data')

        try:
            response1 = self._database.complete_transaction(user_data['ids'],
                                                            user_data['first_name'],
                                                            user_data['last_name'],
                                                            user_data['telegram_name'],
                                                            user_data['date_message'],
                                                            number_temp=7).status

            response2 = self._database.complete_transaction(user_data['ids'],
                                                            user_data['logging'],
                                                            user_data['logging_type'],
                                                            user_data['logging_stage'],
                                                            number_temp=8).status

            response3 = self._database.complete_transaction(user_data['ids'], number_temp=9).status

        except KeyError:
            return dataclass.ResultOperation(status=False, description='not all user_data')

        if False in (response1, response2, response3):
            return dataclasses.ResultOperation(status=False, description='DB error')

        return dataclass.ResultOperation()

    def init_user(self, ids, fname, lname, telegname, date_message):
        response = self.add_user_entry(ids=ids,
                                       first_name=fname,
                                       last_name=lname,
                                       telegram_name=telegname,
                                       date_message=date_message,
                                       logging=True,
                                       logging_type=DEFAULT_LOGGING_TYPE,
                                       logging_stage=DEFAULT_LOGGING_STAGE
                                       )

        if not response.status:
            return dataclass.ResultOperation(status=False, description='_database error')

        return dataclass.ResultOperation()

    def del_main_message_from_db(self, ids, type_message):
        if not (ids or type_message):
            return dataclass.ResultOperation(status=False, description='not full args')

        response = self._database.complete_transaction(ids, type_message, number_temp=15)

        if not response.status:
            return dataclass.ResultOperation(status=False, description='deleting error')

        return dataclass.ResultOperation()


class Database(DBGetMethods, DBSetMethods):
    all_cities: dict
    _database: sqlexecutor.Execute

    def __init__(self):

        db_settings = json_getters.get_setings_db()

        if not db_settings.status:
            raise RuntimeError('json getting error')

        self._database = sqlexecutor.Execute(NameDB=db_settings.object['namedb'],
                                             password=db_settings.object['password'],
                                             user=db_settings.object['user'],
                                             debug=DBDEBUG
                                             )

        if not self._database:
            raise ConnectionError('error with initializing database')

        self.all_cities = self._get_cities().object

        if not self.all_cities:
            raise RuntimeError('error with database (_get_cities)')

    def stop_working(self):
        if self._database:
            self._database.exit()
