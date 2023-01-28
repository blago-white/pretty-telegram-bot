from typing import Union

from src.bot.bin import dataclass
from src.bot.bin.jsons import json_getters
from src.bot.db import sqlexecutor
from src.etc.config import (MAX_LEN_SAMPLING_CITIES,
                            STATEMENT_FOR_STAGE,
                            LIMIT_REGISTRATION_STAGES,
                            MEDIUM_LEN_SAMPLING_CITIES,
                            TYPES_MAIN_MESSAGES,
                            DEFAULT_LANG)


class DBGetMethods:

    @staticmethod
    def _search_city(string_idx: int, city: str, cities: dict[str], length_border: int):
        result = [correct_city.capitalize()
                  for correct_city in cities
                  if correct_city[:string_idx] == city[:string_idx]
                  ]

        if len(result) <= length_border:
            return [cities[correct_city]
                    for correct_city in cities
                    if correct_city[:string_idx] == city[:string_idx]
                    ]

        return result

    def get_similar_cities(self, city: str) -> dataclass.ResultOperation:
        try:
            if not city:
                return dataclass.ResultOperation(status=False)

        except:
            return dataclass.ResultOperation(status=False)

        result_list = []

        for string_idx in range(1, len(city) + 1):

            result_list = self._search_city(string_idx=string_idx,
                                            city=city,
                                            cities=self.all_cities,
                                            length_border=MEDIUM_LEN_SAMPLING_CITIES)

            if not result_list:
                if string_idx == 1:
                    return dataclass.ResultOperation(obj=[])

                return dataclass.ResultOperation(obj=self._search_city(string_idx=string_idx - 1,
                                                                       city=city,
                                                                       cities=self.all_cities,
                                                                       length_border=MEDIUM_LEN_SAMPLING_CITIES))

        return dataclass.ResultOperation(obj=result_list)

    def get_logging_info(self, ids: int) -> dataclass.ResultOperation:
        response = self._database.complete_transaction(ids, number_temp=1)

        if not response.status:
            return dataclass.ResultOperation(False, 'database error')

        if not len(response.object):
            return dataclass.ResultOperation(desc='not info')

        return dataclass.ResultOperation(obj=response.object[0])

    def get_main_message(self, ids, type_message):
        if not (ids or type_message):
            return dataclass.ResultOperation(status=False, desc='not full args')

        id_msg = self._database.complete_transaction(ids, type_message, number_temp=16)

        if not id_msg.object:
            return dataclass.ResultOperation(status=True, desc='mes not found')

        return dataclass.ResultOperation(obj=int(id_msg.object[0][0]))

    def _get_cities(self):

        result = {}
        response = self._database.complete_transaction('cities', number_temp=17)

        if not response.status:
            return dataclass.ResultOperation(status=False, desc='database error')

        for city in response.object:
            region = city[1]
            region = region.replace('область',
                                    'обл.').replace('Республика',
                                                    'Респ.').replace('автономный округ',
                                                                     'a.о.').replace('автономная область',
                                                                                     'a.обл.')

            result.update({str.lower(city[0]): f'<b>{city[0]}</b> [{region}]'})

        return dataclass.ResultOperation(obj=result)

    def get_user_lang_code(self, ids):
        lang_response = self.get_user_data_by_table(ids=ids, table_name='users')

        if lang_response.object:
            if lang_response.object[-1]:
                return lang_response.object[-1][-1]

        return DEFAULT_LANG

    def get_user_data_by_table(self, ids: int, table_name: str) -> dataclass.ResultOperation:
        return self._database.complete_transaction(table_name, ids, number_temp=19)

    def get_user_entrys(self, ids):
        if self.get_user_data_by_table(ids=ids, table_name='users').status:

            results = [self.get_user_data_by_table(ids=ids, table_name=name) for name in
                       self._database.USER_DATA_TABLES]

            for r in results:
                if not r.status:
                    return dataclass.ResultOperation(status=False, desc='database error')

            results = [result.object for result in results]

            for idx, dbdata in enumerate(results):
                if len(dbdata):
                    results[idx] = results[idx][0]

            result = {}
            for idx, table_name in enumerate(self._database.USER_DATA_TABLES):
                result.update({table_name: results[idx]})

            return dataclass.ResultOperation(obj=result, desc='ann have')

        else:
            return dataclass.ResultOperation('not ann')


class DBSetMethods:

    def change_state_logging(self, ids: int, logtype=None, logstage=None, stop_logging: bool = None):
        if stop_logging:
            response = self._database.complete_transaction(ids, number_temp=3)
            if not response.status:
                return dataclass.ResultOperation(status=False, desc='_database error 1')

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
            dataclass.ResultOperation(status=False, desc='_database error 3')

        return dataclass.ResultOperation()

    def set_user_lang(self, ids: int, lang_code: str):
        self._database.complete_transaction(lang_code, ids, number_temp=21)

    def save_photo(self, ids: int, file_id, upd=False):
        if not upd:
            response = self._database.complete_transaction(ids, file_id, number_temp=5)

        else:
            response = self._database.complete_transaction(file_id, ids, number_temp=6)

        return dataclass.ResultOperation(obj=response)

    def add_main_message_to_db(self, ids: int, id_message: int, type_message: int):

        if not (ids or id_message or type_message) or type_message not in TYPES_MAIN_MESSAGES:
            return dataclass.ResultOperation(status=False, desc='args')

        self._database.complete_transaction(ids, id_message, int(type_message), number_temp=14)

        return dataclass.ResultOperation()

    def record_user_data_by_stage(self, message_text, ids, logstage, update=False):

        type_err_temp = 'not correct type of %s (need %s) given %s'

        if logstage == 1:

            try:
                self._database.complete_transaction(int(message_text), ids, number_temp=10)

            except TypeError:
                return dataclass.ResultOperation(status=False, desc=type_err_temp % ('age', int, type(message_text)))

        elif logstage == 2:
            try:
                response = self._database.complete_transaction(str(message_text), ids, number_temp=11)

            except TypeError:
                return dataclass.ResultOperation(status=False, desc=type_err_temp % ('city', str, type(message_text)))

            if not response.status:
                return dataclass.ResultOperation(status=False, desc='_database error')

        elif logstage == 3:

            try:
                response = self._database.complete_transaction(bool(message_text), ids, number_temp=12)

            except TypeError:
                return dataclass.ResultOperation(status=False, desc=type_err_temp % ('male', bool, type(message_text)))

            if not response.status:
                return dataclass.ResultOperation(status=False, desc='_database error')

        elif logstage == 4:

            try:
                processed_text = message_text.replace("'", "''").replace("/", "")
                response = self._database.complete_transaction(processed_text, ids, number_temp=13)

            except TypeError:
                return dataclass.ResultOperation(status=False, desc=type_err_temp % ('desc', str, type(message_text)))

            if not response.status:
                return dataclass.ResultOperation(status=False, desc='_database error')

        elif logstage == 5:

            try:
                response = self.save_photo(ids=ids, file_id=str(message_text), upd=update)

            except TypeError:
                return dataclass.ResultOperation(status=False, desc=type_err_temp % ('ph_id', str, type(message_text)))

            if not response.status:
                return dataclass.ResultOperation(status=False, desc='save photo error 1')

        return dataclass.ResultOperation()

    def del_user_annotations(self, ids):
        for dbname in self._database.TABLES:
            self._database.complete_transaction(dbname, ids, number_temp=20)

    def add_user_entry(self, **user_data):

        if len(user_data) < 8:
            return dataclass.ResultOperation(status=False, desc='not all user_data')

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
            return dataclass.ResultOperation(status=False, desc='not all user_data')

        if False in (response1, response2, response3):
            return dataclasses.ResultOperation(status=False, desc='DB error')

        return dataclass.ResultOperation()

    def init_user(self, ids, fname, lname, telegname, date_message):
        response = self.add_user_entry(ids=ids,
                                       first_name=fname,
                                       last_name=lname,
                                       telegram_name=telegname,
                                       date_message=date_message,
                                       logging=True,
                                       logging_type=1,
                                       logging_stage=0
                                       )

        if not response.status:
            return dataclass.ResultOperation(status=False, desc='_database error')

        return dataclass.ResultOperation()

    def del_main_message_from_db(self, ids, type_message):
        if not (ids or type_message):
            return dataclass.ResultOperation(status=False, desc='not full args')

        response = self._database.complete_transaction(ids, type_message, number_temp=15)

        if not response.status:
            return dataclass.ResultOperation(status=False, desc='deleting error')

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
                                             debug=db_settings.object['debug']
                                             )

        if not self._database:
            raise ConnectionError('error with initializing database')

        self.all_cities = self._get_cities().object

        if not self.all_cities:
            raise RuntimeError('error with database (_get_cities)')

    def stop_working(self):
        if self._database:
            self._database.exit()
