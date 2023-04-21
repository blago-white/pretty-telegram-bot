import datetime
import psycopg2.extras
from typing import Union

from . import _template_placeholder

from ...db import connections, executor
from ..utils.exceptions import exceptions

from ..config.dbconfig import *
from ..config.recording_stages import *

__all__ = ['BotDatabase']


class UserRecording:
    executor: executor.Excecutor

    def get_recording_condition(self, user_id: int) -> Union[list[tuple], None]:
        response = self.executor.execute_query(_template_placeholder.fill_sql_template(user_id, number_temp=1))
        if response:
            return response[0]
        raise exceptions.UserDataNotFoundException

    def stop_recording(self, user_id: int) -> None:
        self.executor.execute_query(_template_placeholder.fill_sql_template(user_id, number_temp=3))

    def increase_recording_stage(self, user_id: int) -> None:
        recording, record_type, record_stage = self.get_recording_condition(user_id=user_id)
        record_stage = _increase_stage_recording(record_stage)
        if recording:
            self.executor.execute_query(
                _template_placeholder.fill_sql_template(record_type, record_stage, user_id, number_temp=4)
            )

    def start_recording(self, user_id: int, record_type: str, record_stage: str) -> None:
        self.executor.execute_query(
            _template_placeholder.fill_sql_template(record_type, record_stage, user_id, number_temp=4)
        )


class UserSpecifiedBuffer:
    executor: executor.Excecutor

    def buffering_user_with_params(self, user_id: int) -> None:
        self.executor.execute_query(
            sqlquery=_template_placeholder.fill_sql_template(
                int(user_id), datetime.datetime.now(), True, number_temp=27
            )
        )

    def del_user_from_buffer(self, user_id: int) -> None:
        self.executor.execute_query(sqlquery=_template_placeholder.fill_sql_template(user_id, number_temp=26))


class UserLanguage:
    executor: executor.Excecutor

    def get_user_lang_or_default(self, user_id: int) -> str:
        try:
            return self.get_user_data_by_table(user_id=user_id, table_name='users')[-1][-1]
        except:
            return DEFAULT_LANG

    def change_user_lang(self, user_id: int, lang_code: str) -> None:
        self.executor.execute_query(_template_placeholder.fill_sql_template(lang_code, user_id, number_temp=21))


class UserRecords:
    executor: executor.Excecutor

    def user_exist(self, user_id: int) -> bool:
        return self.executor.execute_query(
                sqlquery=_template_placeholder.fill_sql_template(user_id, number_temp=34)
            )[0][0]

    def add_new_user(self, user_id, fname, lname, telegname, date_message) -> Union[BaseException, None]:
        responses = (
            self.executor.execute_query(_template_placeholder.fill_sql_template(
                user_id, fname, lname, telegname, date_message, number_temp=7)),

            self.executor.execute_query(_template_placeholder.fill_sql_template(
                user_id, number_temp=9))
        )

        if BaseException in responses:
            raise exceptions.SQLSintaxError

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
        user_record = self.executor.execute_query(_template_placeholder.fill_sql_template(user_id, number_temp=30))
        return bool(user_record)

    def delete_user_records(self, user_id: int) -> None:
        for dbname in TABLES:
            self.executor.execute_query(_template_placeholder.fill_sql_template(dbname, user_id, number_temp=20))


class UserSearching:
    executor: executor.Excecutor

    def record_user_searching_param(self, user_id: int, name_param: str, value_param: Union[str, int, bool]) -> None:
        self.executor.execute_query(
            sqlquery=_template_placeholder.fill_sql_template(name_param, value_param, user_id, number_temp=10)
        )

    def get_user_id_without_params(self, user_id: int) -> Union[int, None]:
        users = self.executor.execute_query(_template_placeholder.fill_sql_template(user_id, number_temp=25))
        return users[0][0] if type(users) is list and users else list(tuple())

    def get_user_id_by_params(
            self, user_id: int,
            age_range: psycopg2.extras.NumericRange,
            city: str,
            sex: bool) -> Union[int, None]:
        users = self.executor.execute_query(
            _template_placeholder.fill_sql_template(age_range, city, sex, user_id, number_temp=18)
        )

        return users[0][0] if type(users) is list and users else list(tuple())


class UserPhotos:
    executor: executor.Excecutor

    def get_photo_id(self, user_id: int) -> str:
        photo_id = self.executor.execute_query(_template_placeholder.fill_sql_template(user_id, number_temp=28))
        return photo_id[0][0] if type(photo_id) is list and photo_id else ''

    def update_photo_id(self, user_id: int, file_id: str) -> None:
        self.executor.execute_query(_template_placeholder.fill_sql_template(file_id, user_id, number_temp=6))

    def save_photo_id(self, user_id: int, file_id: str) -> None:
        self.executor.execute_query(_template_placeholder.fill_sql_template(user_id, file_id, number_temp=5))


class UserWishes:
    executor: executor.Excecutor

    def get_user_wishes(self, user_id: int) -> list[tuple]:
        return self.executor.execute_query(_template_placeholder.fill_sql_template(user_id, number_temp=2))[0]

    def record_new_wish_param(self, user_id: int, name_param: str, value_param: Union[str, int, bool]) -> None:
        if name_param in COLUMNS_WITH_WISHES:
            self.executor.execute_query(_template_placeholder.fill_sql_template(
                name_param, value_param, user_id, number_temp=10
            ))


class UserMessages:
    executor: executor.Excecutor

    def get_main_message(self, user_id: int) -> int:
        message_id = self.executor.execute_query(_template_placeholder.fill_sql_template(user_id, number_temp=16))
        return int(message_id[0][0]) if type(message_id) is list and message_id else 0

    def set_main_message_id(self, user_id: int, message_id: int) -> None:
        setting_method = self._setting_function[bool(self.get_main_message(user_id))]
        setting_method(self, user_id=user_id, message_id=message_id)

    def delete_main_message(self, user_id) -> None:
        self.executor.execute_query(_template_placeholder.fill_sql_template(user_id, number_temp=15))

    def _update_main_message_id(self, user_id: int, message_id: int) -> None:
        self.executor.execute_query(_template_placeholder.fill_sql_template(message_id, user_id, number_temp=29))

    def _add_main_message_id(self, user_id: int, message_id: int) -> None:
        self.executor.execute_query(_template_placeholder.fill_sql_template(user_id, message_id, number_temp=14))

    _setting_function = {True: _update_main_message_id,
                         False: _add_main_message_id}


class UserCities:
    executor: executor.Excecutor
    _cities: dict[str] = dict()

    def get_cities(self) -> dict[str]:
        if not self._cities:
            self._set_cities()
        print(self._cities)
        return self._cities

    def _set_cities(self) -> None:
        cities_from_db = self.executor.execute_query(_template_placeholder.fill_sql_template(number_temp=17))
        self._cities = self._reformat_cities_list(cities=cities_from_db)


class DBTables:
    executor: executor.Excecutor

    def get_user_data_by_table(self, user_id: int, table_name: str) -> Union[list[tuple], BaseException, None]:
        return self.executor.execute_query(_template_placeholder.fill_sql_template(table_name,
                                                                                   int(user_id),
                                                                                   number_temp=19))


class BotDatabase(UserRecording,
                  UserSpecifiedBuffer, UserLanguage, UserRecords, UserSearching,
                  UserPhotos, UserWishes, UserMessages, UserCities, DBTables):
    executor: executor.Excecutor
    _postgre_connector: connections.PostgreConnection

    def __init__(self, namedb: str, password: str, user: str):
        self._postgre_connector = connections.PostgreConnection(nameDB=namedb, password=password, user=user)
        self.executor = executor.Excecutor(postgre_connection=self._postgre_connector.get_postgres_connection())

        if (not self.executor) or (not self._postgre_connector):
            raise ConnectionError('error with initializing database')

    def exit(self) -> None:
        if self._postgre_connector:
            self._postgre_connector.exit()


def _increase_stage_recording(stage_recording: str) -> str:
    return STAGES_RECORDING[
        STAGES_RECORDING.index(stage_recording) + 1
        if stage_recording != LAST_REGISTRATION_STAGE else
        STAGES_RECORDING.index(stage_recording)]
