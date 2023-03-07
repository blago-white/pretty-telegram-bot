from typing import Union

from src.prettybot.bot.db import database_assistant
from src.prettybot.dataclass import dataclass
from src.prettybot.bot.messages import tgmessages
from src.prettybot.scripts import supportive
from src.prettybot.bot.callback.callback_keyboards import *
from src.config.pbconfig import *


class LargeMessageTextGenerator:
    _database_operation_assistant: database_assistant.Database

    def __init__(self, database_operation_assistant):
        self._database_operation_assistant = database_operation_assistant

    def generate_profile_body(
            self,
            user_id: int,
            user_lang_code: str
    ) -> str:
        """

        :returns: Dataclasses.ResultOperation object

        """

        age_declination = 'лет'

        account_data = self._database_operation_assistant.get_user_data_by_table(
            user_id=user_id,
            table_name='users_info'
        ).object[0]

        username = self._database_operation_assistant.get_user_data_by_table(
            user_id=user_id,
            table_name='users'
        ).object[0][1]

        print(account_data, '-----')

        if account_data[1] % 10 == 1:
            age_declination = 'год'

        elif 1 < account_data[1] % 10 < 5:
            age_declination = 'года'

        return STATEMENTS_BY_LANG[user_lang_code].profile_templ.format(name=username,
                                                                       age=account_data[1],
                                                                       declination=age_declination,
                                                                       city=account_data[3].capitalize(),
                                                                       desc=account_data[7]
                                                                       )

    def generate_finding_params_message(
            self,
            user_id: int,
            user_lang_code: str) -> Union[str, dataclass.ResultOperation]:

        user_data = self._database_operation_assistant.get_user_wishes(user_id=user_id)

        if not user_data.status:
            return user_data

        user_data = user_data.object
        age_interval = user_data[0]

        return STATEMENTS_BY_LANG[user_lang_code].change_find_params.format(
            user_data[1],
            int(age_interval.lower),
            int(age_interval.upper),
            supportive.convert_sex_type(user_data[2])
        )


class LargeMessageRenderer:
    _database_operation_assistant: database_assistant.Database
    _message_deleter: tgmessages.MessageDeleter
    _message_sender: tgmessages.MessageSender
    _large_message_text_generator: LargeMessageTextGenerator

    def __init__(
            self, database_operation_assistant: database_assistant.Database,
            message_deleter: tgmessages.MessageDeleter,
            message_sender: tgmessages.MessageSender,
            large_message_text_generator: LargeMessageTextGenerator):

        self._database_operation_assistant = database_operation_assistant
        self._message_deleter = message_deleter
        self._message_sender = message_sender
        self._large_message_text_generator = large_message_text_generator

    async def render_profile(
            self, user_id: int,
            user_lang_code: str) -> None:

        profile_photo_id = self._database_operation_assistant.get_user_data_by_table(
            user_id=user_id,
            table_name='photos'
        ).object[0][1]

        current_account_msg_id = self._database_operation_assistant.get_main_message(user_id=user_id,
                                                                                     type_message=PROFILE_MESSAGE_TYPE)

        if current_account_msg_id.object:
            await self._message_deleter.delete_message(user_id=user_id,
                                                       idmes=current_account_msg_id.object,
                                                       )

            self._database_operation_assistant.del_main_message_from_db(user_id=user_id,
                                                                        type_message=PROFILE_MESSAGE_TYPE)

        sending_result = await self._message_sender.send_photo(
            user_id=user_id,
            photo_id=profile_photo_id,
            description=self._large_message_text_generator.generate_profile_body(user_id=user_id,
                                                                                 user_lang_code=user_lang_code),
            keyboard=INLINE_PROFILE_KB[user_lang_code]
        )

        self._database_operation_assistant.add_main_message_to_db(user_id=user_id,
                                                                  id_message=sending_result.object,
                                                                  type_message=PROFILE_MESSAGE_TYPE)

    async def render_finding_message(
            self, user_id: int,
            user_lang_code: str) -> None:
        """
            :param user_id:
            :param user_lang_code:
            :returns: id of sended message
            """
        response_sending = await self._message_sender.send(
            user_id=user_id,
            description=STATEMENTS_BY_LANG[user_lang_code].clarify,
            markup=INLINE_MODE_FINDING_KB[user_lang_code]
        )

        existing_message_id = self._database_operation_assistant.get_main_message(
            user_id=user_id,
            type_message=QUESTION_MESSAGE_TYPE).object

        if existing_message_id:
            await self._message_deleter.delete_message(user_id=user_id, idmes=existing_message_id)

        self._database_operation_assistant.add_main_message_to_db(
            user_id=user_id,
            id_message=response_sending.object,
            type_message=QUESTION_MESSAGE_TYPE
        )

    async def render_clarify_message(
            self, user_id,
            user_lang_code: str) -> None:

        sending_response: dataclass.ResultOperation = await self._message_sender.send(
            user_id=user_id,

            description=self._large_message_text_generator.generate_finding_params_message(
                user_id=user_id,
                user_lang_code=user_lang_code
            ),

            markup=INLINE_CHANGE_PARAMS_FIND_KB[
                user_lang_code])

        existing_message_id = self._database_operation_assistant.get_main_message(
            user_id=user_id,
            type_message=QUESTION_MESSAGE_TYPE).object

        if existing_message_id:
            await self._message_deleter.delete_message(user_id=user_id, idmes=existing_message_id)

        self._database_operation_assistant.add_main_message_to_db(user_id=user_id,
                                                                  id_message=sending_response.object,
                                                                  type_message=QUESTION_MESSAGE_TYPE)

    async def delete_large_message(
            self, user_id,
            type_message: str) -> None:

        message_id = self._database_operation_assistant.get_main_message(user_id=user_id,
                                                                         type_message=type_message).object

        if message_id:
            await self._message_deleter.delete_message(user_id=user_id, idmes=message_id)
            self._database_operation_assistant.del_main_message_from_db(user_id=user_id, type_message=type_message)
