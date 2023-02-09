"""
Main file of _bot with handlers
"""
import asyncio

import aiogram

from src.bot.callback import callbacks
from src.bot.db import database_assistant
from src.bot.telegram.script import message_manager
from src.bot.telegram.script import helper_bot_scripts
from src.conf.config import *

from src.bot.simple import decorators

__all__ = ['CallbackHandler', 'callback_handler', 'MessageHandler', 'start_handler', 'handle_photo', 'text_handler',
           'help_handler', 'restart_bot_handler', 'change_language_handler']


class CallbackHandler:
    _database_operation_assistant: database_assistant.Database
    _callback_handler: callbacks.CallbackHandler

    def __init__(
            self,
            database_operation_assistant: database_assistant.Database,
            callback_handler: callbacks.CallbackHandler):
        self._database_operation_assistant = database_operation_assistant
        self._callback_handler = callback_handler

    async def callback_handler(self, callback_query: aiogram.types.CallbackQuery):
        """

        all callbacks handled by this function

        """

        payload = callbacks.unpack_playload(payload_string=callback_query.data)
        user_id = callback_query.from_user.id
        user_lang_code = self._database_operation_assistant.get_user_lang_code(ids=user_id)

        type_logging, stage_logging = self._database_operation_assistant.get_logging_info(ids=user_id).object[-2:]

        await self._callback_handler.process_callback_by_id(payload=payload,
                                                            ids=user_id,
                                                            idquery=callback_query.id,
                                                            message=callback_query.message.message_id,
                                                            user_lang_code=user_lang_code,
                                                            stage_logging=stage_logging,
                                                            type_logging=type_logging)


class MessageHandler:
    _database_operation_assistant: database_assistant.Database
    _message_sender: message_manager.MessageSender
    _message_deleter: message_manager.MessageDeleter
    _bot_helper_scripts_: helper_bot_scripts.HelperScripts

    def __init__(
            self,
            database_operation_assistant: database_assistant.Database,
            message_sender: message_manager.MessageSender,
            message_deleter: message_manager.MessageDeleter,
            bot_helper_scripts_: helper_bot_scripts.HelperScripts):

        if not (type(database_operation_assistant) == database_assistant.Database
                and type(message_sender) == message_manager.MessageSender
                and type(bot_helper_scripts_) == helper_bot_scripts.HelperScripts
                and type(message_deleter) == message_manager.MessageDeleter):
            raise TypeError('Not correct class(-es) in arguments')

        self._database_operation_assistant = database_operation_assistant
        self._message_sender = message_sender
        self._message_deleter = message_deleter
        self._bot_helper_scripts = bot_helper_scripts_

    @decorators.prehandler
    async def start_handler(self, message: aiogram.types.Message, user_id: int):

        user_logging_condition = self._database_operation_assistant.get_logging_info(ids=user_id)

        print(user_logging_condition.__dict__)
        print(message.date, '--+', type(message.date))

        if not user_logging_condition.status:
            await self._message_sender.send_except_message(user_id=user_id)
            return

        if not user_logging_condition.object:
            response = self._database_operation_assistant.add_user_entry(ids=user_id,
                                                                    fname=message.from_user.first_name,
                                                                    lname=message.from_user.last_name,
                                                                    telegname=message.chat.username,
                                                                    date_message=message.date
                                                                    )

            if not response.status:
                await self._message_sender.send_except_message(user_id=user_id)
                return

            welcome_sending_response = await self._message_sender.send(user_id=user_id,
                                                                       description=BASE_STATEMENTS.welcome.format(
                                                                           message.from_user.first_name)
                                                                       )

            entry_sending_response = await self._message_sender.send(user_id=user_id,
                                                                     description=STATEMENTS_BY_LANG[
                                                                         DEFAULT_LANG
                                                                     ].entry_registration
                                                                     )

            await self._message_deleter.delete_message(user_id=user_id,
                                                       idmes=message.message_id,
                                                       )

            self._database_operation_assistant.add_main_message_to_db(ids=user_id,
                                                                      id_message=welcome_sending_response.object,
                                                                      type_message=2)

            self._database_operation_assistant.add_main_message_to_db(ids=user_id,
                                                                      id_message=entry_sending_response.object,
                                                                      type_message=1)

        elif user_logging_condition.object:

            user_lang_code = self._database_operation_assistant.get_user_lang_code(ids=user_id)

            if not user_logging_condition.object[0]:
                await self._bot_helper_scripts.render_profile(user_id=user_id, user_lang_code=user_lang_code)
                await self._message_deleter.delete_message(user_id=user_id, idmes=message.message_id)

            else:
                sending_response = await self._message_sender.send(user_id=user_id,
                                                                   description=STATEMENTS_BY_LANG[user_lang_code].help)

                await self._message_deleter.delete_message(user_id=user_id, idmes=message.message_id)
                await self._bot_helper_scripts.start_delay(LONG_DELAY)
                await self._message_deleter.delete_message(user_id=user_id, idmes=sending_response.object)

    @decorators.prehandler
    async def handle_photo(self, message: aiogram.types.Message, user_id: int):
        user_loging_condition = self._database_operation_assistant.get_logging_info(ids=user_id)

        if not user_loging_condition.status or len(user_loging_condition.object) < 2:
            await self._message_sender.send_except_message(user_id=user_id)
            return

        try:
            logging, type_logging, stage_logging = user_loging_condition.object

        except:
            await self._message_sender.send_except_message(user_id=user_id)
            return

        if logging:

            user_lang_code = self._database_operation_assistant.get_user_lang_code(ids=user_id)

            if stage_logging == 5:
                photo_id = message.photo[0]['file_id']

                statement_response = self._bot_helper_scripts.get_statement_by_stage(
                    message=message,
                    logstage=stage_logging,
                    user_lang_code=user_lang_code
                )

                if statement_response.status:
                    self._database_operation_assistant.record_user_data_by_stage(ids=user_id,
                                                                                 message_text=photo_id,
                                                                                 logstage=stage_logging,
                                                                                 logtype=type_logging,
                                                                                 update=True if type_logging == 2 else False)

                    await self._bot_helper_scripts.render_profile(user_id=user_id,
                                                                  user_lang_code=user_lang_code,
                                                                  )

                    self._database_operation_assistant.change_state_logging(ids=user_id, stop_logging=True)

                await self._bot_helper_scripts.delete_main_message(user_id=user_id,
                                                                   type_message=1)

            else:
                await self._bot_helper_scripts.delete_main_message(user_id=user_id,
                                                                   type_message=1)

        await self._message_deleter.delete_message(user_id=message.from_user.id,
                                                   idmes=message.message_id)

    @decorators.prehandler
    async def text_handler(self, message: aiogram.types.Message, user_id: int):

        user_logging_data = self._database_operation_assistant.get_logging_info(ids=user_id)

        if not user_logging_data.status or len(user_logging_data.object) < 3:
            await self._message_sender.send_except_message(user_id=user_id)
            return

        if not user_logging_data.object:
            await self._message_sender.send_except_message(user_id=user_id,
                                                           description=STATEMENTS_BY_LANG[DEFAULT_LANG].start_warn)

            return

        _, type_logging, stage_logging = user_logging_data.object
        sending_response = None

        if user_logging_data.object[-1] in STAGE_BLOCKED_TEXT_MESSAGES:
            pass

        elif user_logging_data.object[0]:
            user_lang_code = self._database_operation_assistant.get_user_lang_code(ids=user_id)

            statement = self._bot_helper_scripts.get_statement_by_stage(message=message,
                                                                        logstage=stage_logging,
                                                                        user_lang_code=user_lang_code)

            if stage_logging == STAGE_BLOCKED_TEXT_MESSAGES:
                if stage_logging == 3:
                    sending_response = await self._message_sender.send(
                        user_id=user_id,
                        description=STATEMENT_FOR_STAGE[stage_logging],
                        markup=callbacks.inline_kb_set_sex_by_lang[user_lang_code]
                    )

            if statement.status:

                if type_logging == 1:

                    markup_for_stage = callbacks.get_inline_keyboard_by_stage(stage=stage_logging)

                    if statement.object:
                        if stage_logging:
                            if type(markup_for_stage) is dict:
                                sending_response = await self._message_sender.send(
                                    user_id=user_id,
                                    description=statement.object,
                                    markup=markup_for_stage[user_lang_code]
                                )

                            else:
                                sending_response = await self._message_sender.send(
                                    user_id=user_id,
                                    description=statement.object
                                )

                            self._database_operation_assistant.change_state_logging(ids=user_id,
                                                                                    logtype=type_logging,
                                                                                    logstage=stage_logging + 1)

                if type_logging == 2:
                    await self._bot_helper_scripts.render_profile(user_id=user_id,
                                                                  user_lang_code=user_lang_code,
                                                                  )

                    self._database_operation_assistant.change_state_logging(ids=user_id, stop_logging=True)

                if type_logging == 3:
                    pass

                self._database_operation_assistant.record_user_data_by_stage(ids=user_id,
                                                                             message_text=message.text,
                                                                             logstage=stage_logging,
                                                                             logtype=type_logging)

            else:
                if statement.object:
                    sending_response = await self._message_sender.send_except_message(user_id=user_id,
                                                                                      user_lang_code=user_lang_code,
                                                                                      description=statement.object)

            await self._bot_helper_scripts.delete_main_message(user_id=user_id,
                                                               type_message=1)

            if sending_response and sending_response.status:
                self._database_operation_assistant.add_main_message_to_db(ids=user_id,
                                                                          id_message=sending_response.object,
                                                                          type_message=1)

        await self._message_deleter.delete_message(user_id=user_id,
                                                   idmes=message.message_id)

    @decorators.prehandler
    async def help_handler(self, message: aiogram.types.Message, user_id: int):
        user_lang_code = self._database_operation_assistant.get_user_lang_code(ids=user_id)
        sending_response = await self._message_sender.send(user_id=user_id,
                                                           description=STATEMENTS_BY_LANG[
                                                               user_lang_code].help
                                                           )

        await self._message_deleter.delete_message(user_id=user_id, idmes=message.message_id)

        await self._bot_helper_scripts.start_delay(5)

        await self._message_deleter.delete_message(user_id=user_id,
                                                   idmes=sending_response.object)

    @decorators.prehandler
    async def restart_bot_handler(self, message: aiogram.types.Message, user_id: int):

        delete_tasks = list()

        for type_main_message in TYPES_MAIN_MESSAGES:
            delete_tasks.append(asyncio.create_task(self._bot_helper_scripts.delete_main_message(
                user_id=user_id,
                type_message=type_main_message)
            ))

        await asyncio.gather(*delete_tasks)

        self._database_operation_assistant.del_user_annotations(ids=user_id)
        await self._message_deleter.delete_message(user_id=user_id, idmes=message.message_id)

    @decorators.prehandler
    async def change_language_handler(self,
                                      message: aiogram.types.Message,
                                      user_id: int):

        self._database_operation_assistant.change_user_lang(ids=user_id, lang_code=message.text[1:3])

        user_lang_code = self._database_operation_assistant.get_user_lang_code(ids=user_id)

        await self._message_sender.send(user_id=user_id,
                                        description=STATEMENTS_BY_LANG[user_lang_code].change_lang_good)

        await self._message_deleter.delete_message(user_id=user_id, idmes=message.message_id)
        await self._bot_helper_scripts.start_delay(delay=DEFAULT_DELAY)
        await self._message_deleter.delete_message(user_id=user_id, idmes=message.message_id + 1)
