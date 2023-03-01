import aiogram

from src.conf.config import STAGE_BY_PAYLOAD, STATEMENTS_BY_LANG
from src.bot.simple import dataclass
from src.bot.db import database_assistant
from src.bot.telegram.script import message_manager
from src.bot.telegram.script.helper_bot_scripts import HelperScripts
from src.bot.callback.callback_keyboards import (inline_profile_kb_by_lang,
                                                 inline_kb_change_prof_by_lang,
                                                 inline_kb_set_sex_by_lang,
                                                 inline_empty_kb,
                                                 inline_kb_mode_finding_by_lang,
                                                 inline_kb_change_params_by_lang)

from src.conf.config import *


def unpack_playload(payload_string: str) -> dict:
    return dict(type_request=payload_string.split('%')[0],
                type_requested_operation=payload_string.split('%')[1])


def get_inline_keyboard_by_stage(stage: int, registration: bool = True):
    if registration:
        if stage == 2:
            return inline_kb_set_sex_by_lang

        else:
            return inline_empty_kb

    elif not registration:
        if stage == 3:
            return inline_kb_set_sex_by_lang

        else:
            return inline_empty_kb


class CallbackHandler:
    _database_operation_assistant: database_assistant.DatabaseScripts
    bot: aiogram.Bot
    _message_sender: message_manager.MessageSender
    _bot_helper_scripts: HelperScripts

    def __init__(
            self,
            database_operation_assistant: database_assistant.DatabaseScripts,
            bot: aiogram.Bot,
            message_sender: message_manager.MessageSender,
            bot_helper_scripts: HelperScripts
    ):

        if not (type(database_operation_assistant) == database_assistant.DatabaseScripts
                and type(bot) == aiogram.Bot
                and type(message_sender) == message_manager.MessageSender
                and type(bot_helper_scripts) == HelperScripts):
            raise ValueError('Not correct type of given to __init__ arguments check type hints')

        self._database_operation_assistant = database_operation_assistant
        self.bot = bot
        self._message_sender = message_sender
        self._bot_helper_scripts = bot_helper_scripts

    async def process_callback_by_id(
            self,
            payload: dict,
            user_id: int,
            idquery: int,
            message: int,
            user_lang_code: str,
            stage_logging: int = None,
            type_logging: int = None,
            alert_text=None) -> dataclass.ResultOperation:

        """

        :param payload: payload from callback query
        :param user_id: integer id tg
        :param idquery: integer id query
        :param message: aiogram message
        :param user_lang_code: user-language
        :param stage_logging: stage of logging user
        :param type_logging: type of logging user
        :param alert_text: string, alert text

        :retuens: Dataclasses.ResultOperation object

        """

        if alert_text:
            await self.bot.answer_callback_query(idquery, text=text, show_alert=True)

        else:
            await self.bot.answer_callback_query(idquery)

        type_request, type_requested_operation = payload.values()
        sending_response = None

        if type_request == 'main':
            if type_requested_operation == 'change_profile_data':
                await self.bot.edit_message_reply_markup(chat_id=user_id,
                                                         message_id=message,
                                                         reply_markup=inline_kb_change_prof_by_lang[user_lang_code])

            elif type_requested_operation == 'start_find':
                sending_response = await self._bot_helper_scripts.render_finding_message(user_id=user_id,
                                                                                         user_lang_code=user_lang_code)

                await self._bot_helper_scripts.delete_main_message(user_id=user_id,
                                                                   type_message=PROFILE_MESSAGE_TYPE)

            elif type_requested_operation == 'back':
                await self._bot_helper_scripts.render_profile(user_id=user_id,
                                                              user_lang_code=user_lang_code)

                await self._bot_helper_scripts.delete_main_message(user_id=user_id,
                                                                   type_message=QUESTION_MESSAGE_TYPE)

        elif type_request in ('change', 'changewish'):
            if type_requested_operation != 'back':

                callback_markup = get_inline_keyboard_by_stage(
                    stage=STAGE_BY_PAYLOAD[type_requested_operation],
                    registration=False
                )

                if type_request == 'change':
                    sending_response = await self._message_sender.send(
                        user_id=user_id,
                        description=QUESTION_STATEMENT_BY_CALLBACK_PAYLOAD[
                            type_requested_operation
                        ][user_lang_code],
                        markup=callback_markup[user_lang_code]
                    )

                elif type_request == 'changewish':
                    sending_response = await self._message_sender.send(
                        user_id=user_id,
                        description=QUESTION_STATEMENT_BY_CALLBACK_PAYLOAD_FINDING[
                            type_requested_operation
                        ][user_lang_code],
                        markup=callback_markup[user_lang_code]
                    )

                await self._bot_helper_scripts.delete_main_message(user_id=user_id,
                                                                   type_message=QUESTION_MESSAGE_TYPE)

            elif type_requested_operation == 'back':
                await self.bot.edit_message_reply_markup(chat_id=user_id,
                                                         message_id=message,
                                                         reply_markup=inline_profile_kb_by_lang[user_lang_code])

            if type_requested_operation in STAGE_BY_PAYLOAD.keys():
                stage = STAGE_BY_PAYLOAD[payload.get('type_requested_operation')]

                self._database_operation_assistant.change_state_logging(user_id=user_id,
                                                                        logtype=2 if type_request == 'change' else 3,
                                                                        logstage=stage
                                                                        )

        elif type_request == 'sex':
            if not stage_logging:
                return

            received_sex = self._bot_helper_scripts.convert_sex_type(type_requested_operation)

            self._bot_helper_scripts.record_registration_info(
                user_id=user_id,
                message_text=received_sex,
                logstage=stage_logging,
                logtype=type_logging
            )

            if type_logging == 1:
                sending_response = await self._message_sender.send(user_id=user_id,
                                                                   description=STATEMENTS_BY_LANG[
                                                                       user_lang_code
                                                                   ].q_desc
                                                                   )

                self._database_operation_assistant.change_state_logging(user_id=user_id,
                                                                        logtype=1,
                                                                        logstage=stage_logging + 1)

            elif type_logging == 3:
                sending_response = await self._bot_helper_scripts.render_finding_message(user_id=user_id,
                                                                                         user_lang_code=user_lang_code)

            self._database_operation_assistant.add_main_message_to_db(user_id=user_id,
                                                                      id_message=sending_response.object,
                                                                      type_message=QUESTION_MESSAGE_TYPE)

            await self._bot_helper_scripts.delete_main_message(user_id=user_id,
                                                               type_message=QUESTION_MESSAGE_TYPE)

        elif type_request == 'find':

            if type_requested_operation.split('&')[0] == 'start':
                searching_mode = type_requested_operation.split('&')[1]
                finded_users_ids = []

                if searching_mode == 'spec':
                    searching_settings = self._database_operation_assistant.get_user_wishes(user_id=user_id).object
                    print(searching_settings, '_search_settings- ')
                    finded_users_ids = self._database_operation_assistant.get_users_ids_by_params(user_id=user_id)

                elif searching_mode == 'fast':
                    finded_users_ids = self._database_operation_assistant.get_users_ids_by_params(user_id=user_id)

                if finded_users_ids.object:
                    sending_response = await self._message_sender.send(
                        user_id=user_id,
                        description=STATEMENTS_BY_LANG[user_lang_code].find_successful
                    )

                    #  MESSAGE TO SECOND USER

                    result_second_user_message_id = await self._message_sender.send(
                        user_id=user_id,
                        description=STATEMENTS_BY_LANG[user_lang_code]
                    )

                    # self._database_operation_assistant.del_user_from_buffer(user_id=finded_users_ids.object)

                    # self._database_operation_assistant.add_main_message_to_db(user_id=finded_users_ids.object,
                    #                                                           id_message=result_second_user_message_id,
                    #                                                           type_message=QUESTION_MESSAGE_TYPE)

                    # self._database_operation_assistant.change_chatting_condition(user_id=finded_users_ids.object,
                    #                                                              new_condition=True)

                    self._database_operation_assistant.change_chatting_condition(user_id=user_id,
                                                                                 new_condition=True)

                elif not finded_users_ids.object:
                    if searching_mode == 'spec':
                        sending_response = await self._message_sender.send(
                            user_id=user_id,
                            description=STATEMENTS_BY_LANG[user_lang_code].not_spec_users_warn
                        )

                    elif searching_mode == 'fast':
                        sending_response = await self._message_sender.send(
                            user_id=user_id,
                            description=STATEMENTS_BY_LANG[user_lang_code].not_spec_users_warn
                        )

            elif type_requested_operation == 'clarify':
                sending_response = await self._message_sender.send(user_id=user_id,
                                                                   description=self._bot_helper_scripts.get_change_params(
                                                                       user_id=user_id,
                                                                       user_lang_code=user_lang_code
                                                                   ),
                                                                   markup=inline_kb_change_params_by_lang[
                                                                       user_lang_code])

            elif type_requested_operation == 'back':
                id_finding_window = await self._bot_helper_scripts.render_finding_message(user_id=user_id,
                                                                                          user_lang_code=user_lang_code)
                await self._bot_helper_scripts.delete_main_message(user_id=user_id,
                                                                   type_message=QUESTION_MESSAGE_TYPE)
                self._database_operation_assistant.add_main_message_to_db(user_id=user_id,
                                                                          id_message=id_finding_window.object,
                                                                          type_message=QUESTION_MESSAGE_TYPE)

                return

            await self._bot_helper_scripts.delete_main_message(user_id=user_id, type_message=QUESTION_MESSAGE_TYPE)

        if sending_response:
            if sending_response.object:
                print('---main', type_requested_operation)
                self._database_operation_assistant.add_main_message_to_db(user_id=user_id,
                                                                          id_message=sending_response.object,
                                                                          type_message=QUESTION_MESSAGE_TYPE)
