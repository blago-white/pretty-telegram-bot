import time
from typing import Union
import asyncio
import aiogram.types

from src.prettybot.bot.db import database_assistant
from src.prettybot.dataclass import dataclass
from src.prettybot.bot.messages import tgmessages
from src.prettybot.scripts import supportive
from src.prettybot.bot.asyncioscripts import coroutine_executor
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

        profile_body = self._large_message_text_generator.generate_profile_body(user_id=user_id,
                                                                                user_lang_code=user_lang_code)

        sending_result = await self._message_sender.send_photo(user_id=user_id,
                                                               photo_id=profile_photo_id,
                                                               description=profile_body,
                                                               keyboard=INLINE_PROFILE_KB[user_lang_code]
                                                               )

        await coroutine_executor.execute_coros(
            *[self.delete_large_message(user_id=user_id, type_message=msgtype)
              for msgtype in (PROFILE_MESSAGE_TYPE, QUESTION_MESSAGE_TYPE)])

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
            markup=INLINE_MODE_FINDING_KB[user_lang_code]),

        await self.delete_large_message(user_id=user_id, type_message=QUESTION_MESSAGE_TYPE)

        self._database_operation_assistant.add_main_message_to_db(
            user_id=user_id,
            id_message=response_sending[0].object,
            type_message=QUESTION_MESSAGE_TYPE
        )

    async def render_clarify_message(
            self, user_id,
            user_lang_code: str) -> None:
        fp_body = self._large_message_text_generator.generate_finding_params_message(
            user_id=user_id,
            user_lang_code=user_lang_code
        )

        sending_response = await self._message_sender.send(user_id=user_id,
                                                           description=fp_body,
                                                           markup=INLINE_CHANGE_PARAMS_FIND_KB[user_lang_code])

        await self.delete_large_message(user_id=user_id, type_message=QUESTION_MESSAGE_TYPE)

        self._database_operation_assistant.add_main_message_to_db(user_id=user_id,
                                                                  id_message=sending_response.object,
                                                                  type_message=QUESTION_MESSAGE_TYPE)

    async def render_disappearing_message(
            self, user_id: int,
            user_message_id: int,
            description: str,
            delay_before_deleting: int) -> None:
        sending_response = await self._message_sender.send(
            user_id=user_id,
            description=description)

        await self._message_deleter.delete_message(user_id=user_id, idmes=user_message_id)
        await supportive.start_delay(delay_before_deleting)
        await self._message_deleter.delete_message(user_id=user_id, idmes=sending_response.object)

    async def render_question_message(
            self, user_id: int,
            description: str,
            markup: aiogram.types.InlineKeyboardMarkup = INLINE_EMPTY_KB,
            with_warn: bool = False) -> None:
        sending_response = await (self._message_sender.send_except_message
                                  if with_warn else
                                  self._message_sender.send)(
            user_id=user_id, description=description, markup=markup)

        await coroutine_executor.execute_coros(*[self.delete_large_message(user_id=user_id, type_message=message_type)
                                                 for message_type in (QUESTION_MESSAGE_TYPE, PROFILE_MESSAGE_TYPE)])

        self._database_operation_assistant.add_main_message_to_db(user_id=user_id,
                                                                  id_message=sending_response.object,
                                                                  type_message=QUESTION_MESSAGE_TYPE)

    async def render_start_message(self, user_id: int, user_first_name: str) -> None:
        response_sending = await self._message_sender.send(
            user_id=user_id,
            description=BASE_STATEMENTS.welcome.format(user_first_name)
        )

        self._database_operation_assistant.add_main_message_to_db(
            user_id=user_id,
            type_message=START_MESSAGE_TYPE,
            id_message=response_sending.object
        )

    async def delete_large_message(
            self, user_id,
            type_message: str) -> None:
        message_id = self._database_operation_assistant.get_main_message(user_id=user_id,
                                                                         type_message=type_message).object
        if message_id:
            await self._message_deleter.delete_message(user_id=user_id, idmes=message_id)
