from typing import Union

from src.prettybot.bot.db import database_assistant
from src.prettybot.dataclass import dataclass
from src.prettybot.bot.messages import tgmessages
from src.prettybot.callback.callback_keyboards import *
from src.conf.pbconfig import *


class LargeMessageRenderer:
    _database_operation_assistant: database_assistant.DatabaseScripts
    _message_deleter: tgmessages.MessageDeleter
    _message_sender: tgmessages.MessageSender

    def __init__(
            self, database_operation_assistant: database_assistant.DatabaseScripts,
            message_deleter: tgmessages.MessageDeleter,
            message_sender: tgmessages.MessageSender):

        self._database_operation_assistant = database_operation_assistant
        self._message_deleter = message_deleter
        self._message_sender = message_sender

    async def render_profile(
            self, user_id: int,
            user_lang_code: str,
            account_body: str) -> None:

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
            description=account_body,
            keyboard=INLINE_PROFILE_KB[user_lang_code]
        )

        if not sending_result.status:
            return dataclass.ResultOperation(status=sending_result.status)

        else:
            self._database_operation_assistant.add_main_message_to_db(user_id=user_id,
                                                                      id_message=sending_result.object,
                                                                      type_message=PROFILE_MESSAGE_TYPE)

        return dataclass.ResultOperation()

    async def render_finding_message(
            self, user_id: int,
            user_lang_code: str) -> dataclass.ResultOperation:
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
        return response_sending

    async def delete_large_message(
            self, user_id,
            type_message: str) -> None:

        message_id = self._database_operation_assistant.get_main_message(user_id=user_id,
                                                                         type_message=type_message).object

        if message_id:
            await self._message_deleter.delete_message(user_id=user_id, idmes=message_id)
            self._database_operation_assistant.del_main_message_from_db(user_id=user_id, type_message=type_message)


class LargeMessageTextGenerator:
    _database_operation_assistant: database_assistant.DatabaseScripts

    def __init__(self, database_operation_assistant):
        self._database_operation_assistant = database_operation_assistant

    def generate_profile_body(
            self,
            user_id: int,
            user_lang_code: str
    ) -> Union[dataclass.ResultOperation, str]:
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

        return dataclass.ResultOperation(
            object=STATEMENTS_BY_LANG[user_lang_code].profile_templ.format(name=username,
                                                                           age=account_data[1],
                                                                           declination=age_declination,
                                                                           city=account_data[3].capitalize(),
                                                                           desc=account_data[7]
                                                                           )
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
            self.convert_sex_type(user_data[2])
        )
