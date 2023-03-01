import asyncio
import re
import aiogram
import psycopg2
from typing import Union

from src.bot.simple import dataclass
from src.bot.db.database_assistant import DatabaseScripts
from src.bot.callback import callbacks
from src.bot.telegram.script import message_manager

from src.conf.config import *


class HelperScripts:
    _database_operation_assistant: DatabaseScripts
    _message_deleter: message_manager.MessageDeleter
    _message_sender: message_manager.MessageSender

    def __init__(
            self, database_scripts: DatabaseScripts,
            message_deleter: message_manager.MessageDeleter,
            message_sender: message_manager.MessageSender):

        self._database_operation_assistant = database_scripts
        self._message_deleter = message_deleter
        self._message_sender = message_sender

    @staticmethod
    def get_drop_down_cities_list(cities_list: list):
        if len(cities_list) > MAX_LEN_SAMPLING_CITIES:
            cities_list[MAX_LEN_SAMPLING_CITIES] += BASE_STATEMENTS.overflow
            cities_list = cities_list[:MAX_LEN_SAMPLING_CITIES + 1]

        return BASE_STATEMENTS.city_sep.join(cities_list)

    @staticmethod
    def convert_sex_type(obj: Union[bool, str]):

        if type(obj) == bool:
            return 'man' if obj else 'woman'

        return True if obj == 'man' else False

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

    @staticmethod
    def get_profile_body(
            name: str,
            age: int,
            city: str,
            desc: str,
            user_lang_code: str
    ) -> Union[dataclass.ResultOperation, str]:
        """

        :param name:
        :param age:
        :param city:
        :param desc:
        :param user_lang_code:

        :retuens: Dataclasses.ResultOperation object

        """

        declination = 'лет'

        if age % 10 == 1:
            declination = 'год'

        elif 1 < age % 10 < 5:
            declination = 'года'

        account_text = STATEMENTS_BY_LANG[user_lang_code].profile_templ.format(name=name,
                                                                               age=age,
                                                                               declination=declination,
                                                                               city=city.capitalize(),
                                                                               desc=desc
                                                                               )

        return dataclass.ResultOperation(object=account_text)

    @staticmethod
    async def start_delay(delay: int):

        """
        :param delay: delay in seconds
        :return:
        """

        delay = int(delay)

        if 0 < delay < MAX_DELAY_TIME_SECONDS:
            await asyncio.sleep(delay=delay)

    def record_registration_info(
            self,
            message_text: str,
            user_id: int,
            logtype: int,
            logstage: int,
            update=False):

        if 1 <= logstage <= 4:
            if logtype != 3:
                self._database_operation_assistant.record_user_param(
                    user_id=user_id,
                    name=NAME_COLUMN_BY_LOGSTAGE[logstage],
                    value="'{}'".format(
                        message_text.replace("'", "''").replace("/", "")
                        if type(message_text) == str else message_text
                    ))

            if logstage in WISHES_COLUMNS:
                print(logstage, '-----')
                if logstage == 1:

                    start_range, stop_range = 0, 0

                    if logtype in (1, 2):
                        start_range = int(message_text) - 5
                        stop_range = int(message_text) + 5

                        if start_range < LOWER_AGE_LIMIT:
                            start_range = LOWER_AGE_LIMIT

                        elif stop_range < LOWER_AGE_LIMIT:
                            stop_range = UPPER_AGE_LIMIT

                    elif logtype == 3:
                        age_digits = [i for i in message_text if i.isdigit()][:4]
                        start_range, stop_range = int(''.join(age_digits[:2])), int(''.join(age_digits[2:]))

                    self._database_operation_assistant.record_user_param(
                        user_id=user_id,
                        name='age_wish',
                        value="'{}'::int4range".format(
                            psycopg2.extras.NumericRange(lower=start_range, upper=stop_range, bounds='[]')
                        )
                    )

                    return

                if logstage == 2:
                    message_text = "'" + message_text + "'"

                self._database_operation_assistant.record_user_param(
                    user_id=user_id,
                    name=NAME_COLUMN_BY_LOGSTAGE[logstage] + '_wish',
                    value=message_text
                )

        elif logstage == 5:

            try:
                response = self._database_operation_assistant.save_photo(user_id=user_id, file_id=str(message_text),
                                                                         upd=update)

            except TypeError:
                return dataclass.ResultOperation(status=False,
                                                 description='not correct doc - id')

            if type(response) is BaseException:
                return dataclass.ResultOperation(status=False, description='not correct doc - id')

        return dataclass.ResultOperation()

    def get_change_params(self, user_id: int, user_lang_code: str):
        user_data = self._database_operation_assistant.get_user_wishes(user_id=user_id)

        if not user_data.status:
            return user_data

        user_data = user_data.object
        age_interval = user_data[0]

        return STATEMENTS_BY_LANG[user_lang_code].change_find_params.format(
            user_data[1],
            int(age_interval.lower),
            int(age_interval.upper),
            self.convert_sex_type(user_data[2])
        )

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
                                            cities=self._database_operation_assistant.all_cities,
                                            length_border=MEDIUM_LEN_SAMPLING_CITIES)

            if not result_list:
                if string_idx == 1:
                    return dataclass.ResultOperation(object=[])

                return dataclass.ResultOperation(object=self._search_city(string_idx=string_idx - 1,
                                                                          city=city,
                                                                          cities=self._database_operation_assistant.all_cities,
                                                                          length_border=MEDIUM_LEN_SAMPLING_CITIES))

        return dataclass.ResultOperation(object=result_list)

    def get_statement_by_stage(
            self,
            message: aiogram.types.Message,
            logstage: int,
            user_lang_code: str,
            logtype: int = 1
    ) -> Union[dataclass.ResultOperation, str]:
        """

        :returns ResultOperation()

        status = True if message is good, obj = statement[string]

        """

        text_message = message.text

        if logstage == 1:
            if logtype in (1, 2):
                try:
                    age = int(text_message)

                    if not LOWER_AGE_LIMIT <= age <= UPPER_AGE_LIMIT:
                        return dataclass.ResultOperation(status=False, object=STATEMENTS_BY_LANG[
                            user_lang_code].invalid_t_age)

                    return dataclass.ResultOperation(status=True, object=STATEMENTS_BY_LANG[user_lang_code].q_city)

                except:
                    return dataclass.ResultOperation(status=False,
                                                     object=STATEMENTS_BY_LANG[user_lang_code].invalid_v_age)

            elif logtype == 3:
                if re.search(r'\d+', text_message) is not None:
                    numbers = [i for i in text_message if i.isdigit()]

                    if len(numbers) < 4:
                        return dataclass.ResultOperation(status=False)

                    return dataclass.ResultOperation(status=True)

        elif logstage == 2:
            if str.lower(str(text_message)) not in self._database_operation_assistant.all_cities:

                simular_cities = self.get_similar_cities(city=str.lower(text_message)).object

                if simular_cities:
                    return dataclass.ResultOperation(status=False,
                                                     object=self.get_drop_down_cities_list(
                                                         cities_list=simular_cities)
                                                     )

                return dataclass.ResultOperation(status=False, object=STATEMENTS_BY_LANG[user_lang_code].invalid_citi)

            return dataclass.ResultOperation(status=True, object=STATEMENTS_BY_LANG[user_lang_code].q_sex)

        elif logstage == 4:

            if len(text_message) > MAX_LEN_DESCRIPTION:
                return dataclass.ResultOperation(status=False,
                                                 object=STATEMENTS_BY_LANG[user_lang_code].invalid_l_desc.format(
                                                     len(text_message)
                                                 ))

            return dataclass.ResultOperation(status=True, object=STATEMENTS_BY_LANG[user_lang_code].q_photo)

            # 'last one, send me your future profile photo!'

        elif logstage == 5:
            if message['photo']:
                return dataclass.ResultOperation(status=True)

            # 'send only photo please'
            return dataclass.ResultOperation(status=False, object=STATEMENTS_BY_LANG[user_lang_code].invalid_t_photo)

        raise ValueError(logstage)

    async def render_profile(self, user_id: int, user_lang_code: str) -> None:
        user_data: dict = self._database_operation_assistant.get_user_entrys(user_id=user_id).object
        user, photo, first_name = user_data.get('users_info'), user_data.get('photos'), user_data.get('users')
        first_name = first_name[1]
        photo = photo[1]

        main_msg_id = self._database_operation_assistant.get_main_message(user_id=user_id,
                                                                          type_message=PROFILE_MESSAGE_TYPE)

        if main_msg_id.object:
            self._database_operation_assistant.del_main_message_from_db(user_id=user_id,
                                                                        type_message=PROFILE_MESSAGE_TYPE)
            await self._message_deleter.delete_message(user_id=user_id,
                                                       idmes=main_msg_id.object,
                                                       )

        account_body = self.get_profile_body(
            name=first_name,
            age=user[1],
            city=user[3],
            desc=user[-1],
            user_lang_code=user_lang_code).object

        sending_result = await self._message_sender.send_photo(
            user_id=user_id,
            photo_id=photo,
            description=account_body,
            keyboard=callbacks.inline_profile_kb_by_lang[
                user_lang_code
            ]
        )

        if not sending_result.status:
            return dataclass.ResultOperation(status=False)

        else:
            self._database_operation_assistant.add_main_message_to_db(user_id=user_id,
                                                                      id_message=sending_result.object,
                                                                      type_message=PROFILE_MESSAGE_TYPE)

        return dataclass.ResultOperation()

    async def delete_main_message(self, user_id: int, type_message: int) -> None:
        message_id = self._database_operation_assistant.get_main_message(user_id=user_id,
                                                                         type_message=type_message).object

        if message_id:
            await self._message_deleter.delete_message(user_id=user_id, idmes=message_id)
            self._database_operation_assistant.del_main_message_from_db(user_id=user_id, type_message=type_message)

    async def render_finding_message(self, user_id: int, user_lang_code: str) -> dataclass.ResultOperation:

        """
        :param user_id:
        :param user_lang_code:
        :returns: id of sended message
        """

        response_sending = await self._message_sender.send(
            user_id=user_id,
            description=STATEMENTS_BY_LANG[user_lang_code].clarify,
            markup=callbacks.inline_kb_mode_finding_by_lang[user_lang_code]
        )
        return response_sending
