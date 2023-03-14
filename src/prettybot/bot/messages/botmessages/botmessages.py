from typing import Union
import aiogram.types

from src.prettybot.bot.dbassistant import database_assistant
from src.prettybot.dataclass import dataclass
from src.prettybot.bot.messages import chat_interaction
from src.prettybot.bot.minorscripts import supportive
from src.prettybot.bot.messages.botmessages import rendering_wrappers
from src.prettybot.bot.callback.callback_keyboards import *
from src.config.pbconfig import *


class MainMessageTextGenerator:
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


class MainMessagesRenderer:
    database_operation_assistant: database_assistant.Database
    message_deleter: chat_interaction.MessageDeleter
    _message_sender: chat_interaction.MessageSender
    _main_message_text_generator: MainMessageTextGenerator

    def __init__(
            self, database_operation_assistant: database_assistant.Database,
            message_deleter: chat_interaction.MessageDeleter,
            message_sender: chat_interaction.MessageSender,
            main_message_text_generator: MainMessageTextGenerator):
        self.database_operation_assistant = database_operation_assistant
        self.message_deleter = message_deleter
        self._message_sender = message_sender
        self._main_message_text_generator = main_message_text_generator

    @rendering_wrappers.rendering_completer
    async def render_profile(
            self, user_id: int,
            user_lang_code: str) -> dict[int]:
        profile_photo_id = self.database_operation_assistant.get_photo_id(user_id=user_id)
        if not profile_photo_id:
            return dict(sended_message_id=None)

        profile_body = self._main_message_text_generator.generate_profile_body(user_id=user_id,
                                                                               user_lang_code=user_lang_code)

        message_id = await self._message_sender.send_photo(user_id=user_id,
                                                           photo_id=profile_photo_id,
                                                           description=profile_body,
                                                           keyboard=INLINE_PROFILE_KB[user_lang_code]
                                                           )
        return dict(sended_message_id=message_id.object)

    @rendering_wrappers.rendering_completer
    async def render_finding_message(
            self, user_id: int,
            user_lang_code: str) -> dict[int]:

        sended_messsage_id = await self._message_sender.send(user_id=int(user_id),
                                                             description=STATEMENTS_BY_LANG[user_lang_code].clarify,
                                                             markup=INLINE_MODE_FINDING_KB[user_lang_code])

        return dict(sended_message_id=sended_messsage_id.object)

    @rendering_wrappers.rendering_completer
    async def render_clarify_message(
            self, user_id,
            user_lang_code: str) -> dict[int]:
        fp_body = self._main_message_text_generator.generate_finding_params_message(
            user_id=int(user_id),
            user_lang_code=str(user_lang_code)
        )

        sended_message_id = await self._message_sender.send(user_id=int(user_id),
                                                            description=str(fp_body),
                                                            markup=INLINE_CHANGE_PARAMS_FIND_KB[user_lang_code])

        return dict(sended_message_id=sended_message_id.object)

    @rendering_wrappers.rendering_completer
    async def render_disappearing_message(
            self, user_id: int,
            description: str,
            retrievable_message_id: int,
            delay_before_deleting: int) -> dict[int]:
        sended_message_id = await self._message_sender.send(user_id=int(user_id), description=str(description))
        return dict(
            sended_message_id=int(sended_message_id.object),
            retrievable_message_id=retrievable_message_id,
            delay_before_deleting=delay_before_deleting)

    @rendering_wrappers.rendering_completer
    async def render_main_message(
            self, user_id: int,
            description: str,
            markup: aiogram.types.InlineKeyboardMarkup = INLINE_EMPTY_KB,
            with_warn: bool = False) -> dict[int]:
        sended_message_id = await (self._message_sender.send_except_message
                                   if with_warn else
                                   self._message_sender.send)(
            user_id=user_id, description=description, markup=markup)

        return dict(sended_message_id=sended_message_id.object)

    async def render_start_message(
            self, user_id: int,
            user_first_name: str) -> dict[int]:
        message_id = await self.render_main_message(user_id=user_id,
                                                    description=BASE_STATEMENTS.welcome.format(user_first_name))

        return dict(
            sended_message_id=message_id['sended_message_id']
        )

    async def delete_main_message(self, user_id: int) -> None:
        message_id = self.database_operation_assistant.get_main_message(user_id=int(user_id)).object
        if message_id:
            await self.message_deleter.delete_message(user_id=user_id, idmes=message_id)
            self.database_operation_assistant.del_main_message_from_db(user_id=user_id)
