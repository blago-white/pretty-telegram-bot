import asyncio
import aiogram
from typing import Union

from src.bot.simple import dataclass
from src.conf.config import *

from src.bot.db.database_assistant import Database
from src.bot.callback import callbacks
from src.bot.telegram.script import message_manager


class HelperScripts:
    _database_operation_assistant: Database
    _message_deleter: message_manager.MessageDeleter
    _message_sender: message_manager.MessageSender

    def __init__(
            self, database_scripts: Database,
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

        return True if 'man' else 'woman'

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

    def get_change_params(self, user_id: int, user_lang_code: str):
        user_data = self._database_operation_assistant.get_user_wishes(ids=user_id)

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
            user_lang_code: str
    ) -> Union[dataclass.ResultOperation, str]:
        """

        :returns ResultOperation()

        status = True if message is good, obj = statement[string]

        """

        if logstage == 1:

            try:
                age = int(message.text)

                if not LOWER_AGE_LIMIT <= age <= UPPER_AGE_LIMIT:
                    return dataclass.ResultOperation(status=False, object=STATEMENTS_BY_LANG[
                        user_lang_code].invalid_t_age)

                return dataclass.ResultOperation(status=True, object=STATEMENTS_BY_LANG[user_lang_code].q_city)

            except:
                return dataclass.ResultOperation(status=False, object=STATEMENTS_BY_LANG[user_lang_code].invalid_v_age)

        elif logstage == 2:
            if str.lower(str(message.text)) not in self._database_operation_assistant.all_cities:

                simular_cities = self.get_similar_cities(city=str.lower(message.text)).object

                if simular_cities:
                    return dataclass.ResultOperation(status=False,
                                                     object=self.get_drop_down_cities_list(
                                                         cities_list=simular_cities)
                                                     )

                return dataclass.ResultOperation(status=False, object=STATEMENTS_BY_LANG[user_lang_code].invalid_citi)

            return dataclass.ResultOperation(status=True, object=STATEMENTS_BY_LANG[user_lang_code].q_sex)

        elif logstage == 4:

            if len(message.text) > MAX_LEN_DESCRIPTION:
                return dataclass.ResultOperation(status=False,
                                                 object=STATEMENTS_BY_LANG[user_lang_code].invalid_l_desc.format(
                                                     len(message.text)
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
        user_data: dict = self._database_operation_assistant.get_user_entrys(ids=user_id).object
        user, photo, first_name = user_data.get('users_info'), user_data.get('photos'), user_data.get('users')
        first_name = first_name[1]
        photo = photo[1]

        main_msg_id = self._database_operation_assistant.get_main_message(ids=user_id, type_message=0)

        if main_msg_id.object:
            self._database_operation_assistant.del_main_message_from_db(ids=user_id, type_message=0)
            await self._message_deleter.delete_message(user_id=user_id,
                                                       idmes=main_msg_id.object,
                                                       )

        account_body = self.get_profile_body(name=first_name,
                                             age=user[1],
                                             city=user[3],
                                             desc=user[-1],
                                             user_lang_code=user_lang_code).object

        sending_result = await self._message_sender.send_photo(user_id=user_id,
                                                               photo_id=photo,
                                                               description=account_body,
                                                               keyboard=callbacks.inline_profile_kb_by_lang[
                                                                   user_lang_code
                                                               ]
                                                               )

        if not sending_result.status:
            return dataclass.ResultOperation(status=False)

        else:
            self._database_operation_assistant.add_main_message_to_db(ids=user_id,
                                                                      id_message=sending_result.object,
                                                                      type_message=0)

        return dataclass.ResultOperation()

    async def delete_main_message(self, user_id: int, type_message: int) -> None:
        message_id = self._database_operation_assistant.get_main_message(ids=user_id, type_message=type_message).object

        if message_id:
            await self._message_deleter.delete_message(user_id=user_id, idmes=message_id)
            self._database_operation_assistant.del_main_message_from_db(ids=user_id, type_message=type_message)