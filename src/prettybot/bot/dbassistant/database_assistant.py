import datetime
import psycopg2.extras
from typing import Union

from src.prettybot.db import template_placeholder
from src.prettybot.db import sql_query_executor
from src.prettybot.db import database_connection
from src.prettybot.bot.minorscripts import minor_scripts

from src.config.dbconfig import *
from src.config.recording_stages import *


class UserRecordingCondition:
    executor: sql_query_executor.Excecutor

    def get_recording_condition(self, user_id: int) -> Union[list[tuple], None]:
        response = self.executor.execute_query(template_placeholder.fill_sql_template(user_id, number_temp=1))
        return response[0] if response else None

    def stop_recording(self, user_id: int) -> None:
        self.executor.execute_query(template_placeholder.fill_sql_template(user_id, number_temp=3))

    def increase_recording_stage(self, user_id: int) -> None:
        recording, record_type, record_stage = self.get_recording_condition(user_id=user_id)
        record_stage = supportive.increase_stage_recording(record_stage)

        if recording:
            self.executor.execute_query(
                template_placeholder.fill_sql_template(record_type, record_stage, user_id, number_temp=4)
            )

    def start_recording(self, user_id: int, record_type: str, record_stage: str) -> None:
        self.executor.execute_query(
            template_placeholder.fill_sql_template(record_type, record_stage, user_id, number_temp=4)
        )


class UserChattingCondition:
    executor: sql_query_executor.Excecutor

    def get_chatting_condition(self, user_id: int) -> Union[bool, BaseException]:
        data = self.executor.execute_query(template_placeholder.fill_sql_template(user_id, number_temp=23))
        return data[0][0] if type(data) is list and data else data

    def start_chatting(self, user_id: int) -> None:
        self.executor.execute_query(
            template_placeholder.fill_sql_template(True, int(user_id), number_temp=24)
        )

    def stop_chatting(self, user_id: int) -> None:
        self.executor.execute_query(
            template_placeholder.fill_sql_template(False, int(user_id), number_temp=24)
        )


class UserBuffer:
    executor: sql_query_executor.Excecutor

    def get_user_buffer_status(self, user_id: int) -> bool:
        from_bufer_data = self.executor.execute_query(
            sqlquery=template_placeholder.fill_sql_template('users_searching_buffer', user_id, number_temp=19)
        )

        return True if from_bufer_data else False

    def buffering_user_with_params(self, user_id: int, date_message: datetime.datetime) -> None:
        self.executor.execute_query(
            sqlquery=template_placeholder.fill_sql_template(user_id, date_message, True, number_temp=27)
        )

    def buffering_user_without_params(self, user_id: int, date_message: datetime.datetime) -> None:
        self.executor.execute_query(
            template_placeholder.fill_sql_template(user_id, date_message, False, number_temp=27)
        )

    def del_user_from_buffer(self, user_id: int) -> None:
        self.executor.execute_query(sqlquery=template_placeholder.fill_sql_template(user_id, number_temp=26))


class UserLanguage:
    executor: sql_query_executor.Excecutor

    def get_user_lang_or_default(self, user_id: int) -> str:
        try:
            return self.get_user_data_by_table(user_id=user_id, table_name='users')[-1][-1]
        except:
            return DEFAULT_LANG

    def change_user_lang(self, user_id: int, lang_code: str) -> None:
        self.executor.execute_query(template_placeholder.fill_sql_template(lang_code, user_id, number_temp=21))


class UserRecords:
    executor: sql_query_executor.Excecutor

    def add_new_user(self, user_id, fname, lname, telegname, date_message) -> Union[BaseException, None]:
        responses = (
            self.executor.execute_query(template_placeholder.fill_sql_template(
                user_id, fname, lname, telegname, date_message, number_temp=7)),

            self.executor.execute_query(template_placeholder.fill_sql_template(
                user_id, True, DEFAULT_RECORD_TYPE, DEFAULT_RECORD_STAGE, False, number_temp=8)),

            self.executor.execute_query(template_placeholder.fill_sql_template(
                user_id, number_temp=9))
        )

        return BaseException if BaseException in responses else None

    def get_user_records(self, user_id: int) -> Union[BaseException, None]:
        if self.check_user_exists(user_id=user_id):
            fetch_results = [self.get_user_data_by_table(user_id=user_id, table_name=name) for name in USER_DATA_TABLES]

            if BaseException in fetch_results:
                return BaseException

            for idx, dbdata in enumerate(fetch_results):
                if dbdata:
                    fetch_results[idx] = fetch_results[idx][0]

            return {{table_name: fetch_results[idx]} for idx, table_name in enumerate(USER_DATA_TABLES)}

    def check_user_exists(self, user_id: int) -> bool:
        user_record = self.executor.execute_query(template_placeholder.fill_sql_template(user_id, number_temp=30))
        return bool(user_record)

    def delete_user_records(self, user_id: int) -> None:
        for dbname in TABLES:
            self.executor.execute_query(template_placeholder.fill_sql_template(dbname, user_id, number_temp=20))


class UserSearching:
    executor: sql_query_executor.Excecutor

    def record_user_searching_param(self, user_id: int, name_param: str, value_param: Union[str, int, bool]) -> None:
        self.executor.execute_query(
            sqlquery=template_placeholder.fill_sql_template(name_param, value_param, user_id, number_temp=10)
        )

    def get_user_id_without_params(self, user_id: int) -> Union[int, None]:
        users = self.executor.execute_query(template_placeholder.fill_sql_template(user_id, number_temp=25))
        return users[0][0] if type(users) is list and users else None

    def get_user_id_by_params(self, user_id: int,
                              age_range: psycopg2.extras.NumericRange,
                              city: str,
                              sex: bool) -> Union[int, None]:

        users = self.executor.execute_query(
            template_placeholder.fill_sql_template(age_range, city, sex, user_id, number_temp=18)
        )

        return users[0][0] if type(users) is list and users else None


class UserPhotos:
    executor: sql_query_executor.Excecutor

    def get_photo_id(self, user_id: int) -> str:
        photo_id = self.executor.execute_query(template_placeholder.fill_sql_template(user_id, number_temp=28))
        return photo_id[0][0] if type(photo_id) is list and photo_id else None

    def update_photo_id(self, user_id: int, file_id: str) -> None:
        self.executor.execute_query(template_placeholder.fill_sql_template(file_id, user_id, number_temp=6))

    def save_photo_id(self, user_id: int, file_id: str) -> None:
        self.executor.execute_query(template_placeholder.fill_sql_template(user_id, file_id, number_temp=5))


class UserWishes:
    executor: sql_query_executor.Excecutor

    def get_user_wishes(self, user_id: int) -> list[tuple]:
        return self.executor.execute_query(template_placeholder.fill_sql_template(user_id, number_temp=2))[0]

    def record_new_wish_param(self, user_id: int, name_param: str, value_param: Union[str, int, bool]) -> None:
        if name_param in COLUMNS_WITH_WISHES:
            self.executor.execute_query(template_placeholder.fill_sql_template(
                name_param, value_param, user_id, number_temp=10
            ))


class UserMessages:
    executor: sql_query_executor.Excecutor

    def get_main_message(self, user_id: int) -> int:
        message_id = self.executor.execute_query(template_placeholder.fill_sql_template(user_id, number_temp=16))
        return int(message_id[0][0]) if type(message_id) is list and message_id else None

    def set_main_message_id(self, user_id: int, message_id: int) -> None:
        setting_method = self._setting_function[bool(self.get_main_message(user_id))]
        setting_method(self, user_id=user_id, message_id=message_id)

    def delete_main_message(self, user_id) -> None:
        self.executor.execute_query(template_placeholder.fill_sql_template(user_id, number_temp=15))

    def _update_main_message_id(self, user_id: int, message_id: int) -> None:
        self.executor.execute_query(template_placeholder.fill_sql_template(message_id, user_id, number_temp=29))

    def _add_main_message_id(self, user_id: int, message_id: int) -> None:
        self.executor.execute_query(template_placeholder.fill_sql_template(user_id, message_id, number_temp=14))

    _setting_function = {True: _update_main_message_id,
                         False: _add_main_message_id}


class UserCities:
    executor: sql_query_executor.Excecutor
    _cities: dict[str] = dict()

    def get_cities(self) -> dict[str]:
        if not self._cities:
            self._set_cities()

        return self._cities

    def _set_cities(self) -> None:
        cities_from_db = self.executor.execute_query(template_placeholder.fill_sql_template(number_temp=17))
        self._cities = self._reformat_cities_list(cities=cities_from_db)

    @staticmethod
    def _reformat_cities_list(cities: list) -> dict[str]:
        if type(cities) is not list:
            raise TypeError(str(type(cities)))

        reformated_cities = dict()
        for city in cities:
            name_city, region, _ = city
            for abbreviation in CITY_NAME_ABBREVIATIONS:
                region = region.replace(abbreviation, CITY_NAME_ABBREVIATIONS[abbreviation])

            reformated_cities.update({str.lower(name_city): CITI_LONG_VIEW.format(name_city, region)})

        return reformated_cities


class DBTables:
    executor: sql_query_executor.Excecutor

    def get_user_data_by_table(self, user_id: int, table_name: str) -> Union[list[tuple], BaseException, None]:
        return self.executor.execute_query(template_placeholder.fill_sql_template(table_name, user_id, number_temp=19))


class Database(UserRecordingCondition, UserChattingCondition,
               UserBuffer, UserLanguage, UserRecords, UserSearching,
               UserPhotos, UserWishes, UserMessages, UserCities, DBTables):

    executor: sql_query_executor.Excecutor
    _postgre_connection: database_connection

    def __init__(self, namedb: str, password: str, user: str):
        self._postgre_connection = database_connection.PostgreConnection(nameDB=namedb,
                                                                         password=password,
                                                                         user=user)

        self.executor = sql_query_executor.Excecutor(connection=self._postgre_connection.CONNECTION)

        if (not self.executor) or (not self._postgre_connection):
            raise ConnectionError('error with initializing database')

    def exit(self) -> None:
        if self._postgre_connection:
            self._postgre_connection.exit()
