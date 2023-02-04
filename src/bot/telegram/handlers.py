"""
Main file of _bot with handlers
"""
import asyncio

import aiogram

from src.bot.module import callbacks
from src.bot.db import dbscripts
from src.bot.telegram.script import message_manager, helper_bot_scripts
from src.conf.config import (STATEMENT_FOR_STAGE,
                             STATEMENTS_BY_LANG,
                             TYPES_MAIN_MESSAGES,
                             BASE_STATEMENTS,
                             DEFAULT_LANG,
                             DEFAULT_DELAY,
                             LONG_DELAY,
                             STAGE_BLOCKED_TEXT_MESSAGES)

from src.bot.simple import decorators


class CallbackHandlers:
    database_operation_assistant: dbscripts.Database
    callback_handler: callbacks.CallbackHandler

    async def process_callback_button(self, callback_query: aiogram.types.CallbackQuery):
        """

        all callbacks handled by this function

        """

        payload = self.callback_handler.unpack(payload_string=callback_query.data)
        user_id = callback_query.from_user.id
        user_lang_code = self.database_operation_assistant.get_user_lang_code(ids=user_id)

        stage_logging = None

        if payload.get('type_request') == 'sex':
            stage_logging = self.database_operation_assistant.get_logging_info(ids=user_id).object[-1]

        await self.callback_handler.process_callback_by_id(payload=payload,
                                                           ids=user_id,
                                                           idquery=callback_query.id,
                                                           message=callback_query.message.message_id,
                                                           user_lang_code=user_lang_code,
                                                           stage_logging=stage_logging)


class MessageHandlers:
    database_operation_assistant: dbscripts.Database
    message_manager_: message_manager.MessageManage
    bot_helper_scripts_: helper_bot_scripts.HelperScripts
    callback_handler: callbacks.CallbackHandler

    @decorators.prehandler
    async def send_welcome(self, message: aiogram.types.Message, user_id: int):

        user_logging_condition = self.database_operation_assistant.get_logging_info(ids=user_id)

        if not user_logging_condition.status:
            await self.message_manager_.send_except_message(ids=user_id)
            return

        if not user_logging_condition.object:
            response = self.database_operation_assistant.init_user(ids=user_id,
                                                                   fname=message.from_user.first_name,
                                                                   lname=message.from_user.last_name,
                                                                   telegname=message.chat.username,
                                                                   date_message=message.date
                                                                   )

            if not response.status:
                await self.message_manager_.send_except_message(ids=user_id)
                return

            welcome_sending_response = await self.message_manager_.sender(ids=user_id,
                                                                          description=BASE_STATEMENTS.welcome.format(
                                                                              message.from_user.first_name)
                                                                          )

            entry_sending_response = await self.message_manager_.sender(ids=user_id,
                                                                        description=STATEMENTS_BY_LANG[
                                                                            DEFAULT_LANG
                                                                        ].entry_registration
                                                                        )

            await self.message_manager_.message_scavenger(ids=user_id,
                                                          idmes=message.message_id,
                                                          )

            self.database_operation_assistant.add_main_message_to_db(ids=user_id,
                                                                     id_message=welcome_sending_response.object,
                                                                     type_message=2)

            self.database_operation_assistant.add_main_message_to_db(ids=user_id,
                                                                     id_message=entry_sending_response.object,
                                                                     type_message=1)

        elif user_logging_condition.object:
            user_lang_code = self.database_operation_assistant.get_user_lang_code(ids=user_id)

            sending_response = await self.message_manager_.sender(ids=user_id,
                                                                  description=STATEMENTS_BY_LANG[user_lang_code].help)

            await self.message_manager_.message_scavenger(ids=user_id, idmes=message.message_id)

            await self.bot_helper_scripts_.start_delay(LONG_DELAY)

            await self.message_manager_.message_scavenger(ids=user_id, idmes=sending_response.object)

    @decorators.prehandler
    async def handle_photo(self, message: aiogram.types.Message, user_id: int):
        user_loging_condition = self.database_operation_assistant.get_logging_info(ids=user_id)

        if not user_loging_condition.status or len(user_loging_condition.object) < 2:
            await self.message_manager_.send_except_message(ids=user_id)
            return

        try:
            logging, type_logging, stage_logging = user_loging_condition.object

        except:
            await self.message_manager_.send_except_message(ids=user_id)
            return

        if logging:

            user_lang_code = self.database_operation_assistant.get_user_lang_code(ids=user_id)

            if stage_logging == 5:
                photo_id = message.photo[0]['file_id']

                statement_response = self.bot_helper_scripts_.get_statement_by_stage(
                    message=message,
                    logstage=stage_logging,
                    user_lang_code=user_lang_code
                )

                if statement_response.status:
                    self.database_operation_assistant.record_user_data_by_stage(ids=user_id,
                                                                                message_text=photo_id,
                                                                                logstage=stage_logging,
                                                                                update=True if type_logging == 2 else False)

                    await self.bot_helper_scripts_.render_profile(user_id=user_id,
                                                                  user_lang_code=user_lang_code,
                                                                  message_manager=self.message_manager_)

                    self.database_operation_assistant.change_state_logging(ids=user_id, stop_logging=True)

                await self.bot_helper_scripts_.delete_main_message(message_manager=self.message_manager_,
                                                                   user_id=user_id,
                                                                   type_message=1)

            else:
                await self.bot_helper_scripts_.delete_main_message(message_manager=self.message_manager_,
                                                                   user_id=user_id,
                                                                   type_message=1)

        await self.message_manager_.message_scavenger(ids=message.from_user.id,
                                                      idmes=message.message_id)

    @decorators.prehandler
    async def text_handler(self, message: aiogram.types.Message, user_id: int):

        user_logging_data = self.database_operation_assistant.get_logging_info(ids=user_id)

        if not user_logging_data.status or len(user_logging_data.object) < 3:
            await self.message_manager_.send_except_message(ids=user_id)
            return

        if not user_logging_data.object:
            await self.message_manager_.send_except_message(ids=user_id,
                                                            description=STATEMENTS_BY_LANG[DEFAULT_LANG].start_warn)

            return

        _, type_logging, stage_logging = user_logging_data.object
        sending_response = None

        if user_logging_data.object[0]:
            user_lang_code = self.database_operation_assistant.get_user_lang_code(ids=user_id)

            statement = self.bot_helper_scripts_.get_statement_by_stage(message=message,
                                                                        logstage=stage_logging,
                                                                        user_lang_code=user_lang_code)

            if stage_logging == STAGE_BLOCKED_TEXT_MESSAGES:
                if stage_logging == 3:
                    sending_response = await self.message_manager_.sender(
                        ids=user_id,
                        description=STATEMENT_FOR_STAGE[stage_logging],
                        markup=callbacks.inline_kb_set_sex_by_lang[user_lang_code]
                    )

            if statement.status:

                self.database_operation_assistant.record_user_data_by_stage(ids=user_id,
                                                                            message_text=message.text,
                                                                            logstage=stage_logging)

                if type_logging == 1:

                    markup_for_stage = self.callback_handler.get_inline_keyboard_by_stage(
                        stage=stage_logging
                    )

                    if statement.object:
                        if stage_logging:
                            if type(markup_for_stage) is dict:
                                sending_response = await self.message_manager_.sender(
                                    ids=user_id,
                                    description=statement.object,
                                    markup=markup_for_stage[user_lang_code]
                                )

                            else:
                                sending_response = await self.message_manager_.sender(
                                    ids=user_id,
                                    description=statement.object
                                )

                            self.database_operation_assistant.change_state_logging(ids=user_id,
                                                                                   logtype=type_logging,
                                                                                   logstage=stage_logging + 1)

                if type_logging == 2:
                    await self.bot_helper_scripts_.render_profile(user_id=user_id,
                                                                  user_lang_code=user_lang_code,
                                                                  message_manager=self.message_manager_)

                    self.database_operation_assistant.change_state_logging(ids=user_id, stop_logging=True)

            else:
                if statement.object:
                    sending_response = await self.message_manager_.send_except_message(ids=user_id,
                                                                                       user_lang_code=user_lang_code,
                                                                                       description=statement.object)

            await self.bot_helper_scripts_.delete_main_message(user_id=user_id,
                                                               message_manager=self.message_manager_,
                                                               type_message=1)

            if sending_response and sending_response.status:
                self.database_operation_assistant.add_main_message_to_db(ids=user_id,
                                                                         id_message=sending_response.object,
                                                                         type_message=1)

        await self.message_manager_.message_scavenger(ids=user_id,
                                                      idmes=message.message_id)

    @decorators.prehandler
    async def handler_help(self, message: aiogram.types.Message, user_id: int):
        user_lang_code = self.database_operation_assistant.get_user_lang_code(ids=user_id)
        sending_response = await self.message_manager_.sender(ids=user_id,
                                                              description=STATEMENTS_BY_LANG[
                                                                  user_lang_code].help
                                                              )

        await self.message_manager_.message_scavenger(ids=user_id, idmes=message.message_id)

        await self.bot_helper_scripts_.start_delay(5)

        await self.message_manager_.message_scavenger(ids=user_id,
                                                      idmes=sending_response.object)

    @decorators.prehandler
    async def restart(self, message: aiogram.types.Message, user_id: int):

        delete_tasks = list()

        for type_main_message in TYPES_MAIN_MESSAGES:
            delete_tasks.append(asyncio.create_task(self.bot_helper_scripts_.delete_main_message(
                message_manager=self.message_manager_,
                user_id=user_id,
                type_message=type_main_message)
            ))

        await asyncio.gather(*delete_tasks)

        self.database_operation_assistant.del_user_annotations(ids=user_id)
        await self.message_manager_.message_scavenger(ids=user_id, idmes=message.message_id)

    @decorators.prehandler
    async def change_language(self, message: aiogram.types.Message, user_id: int):

        self.database_operation_assistant.change_user_lang(ids=user_id, lang_code=message.text[1:3])

        user_lang_code = self.database_operation_assistant.get_user_lang_code(ids=user_id)

        await self.message_manager_.sender(ids=user_id,
                                           description=STATEMENTS_BY_LANG[user_lang_code].change_lang_good)

        await self.message_manager_.message_scavenger(ids=user_id, idmes=message.message_id)
        await self.bot_helper_scripts_.start_delay(delay=DEFAULT_DELAY)
        await self.message_manager_.message_scavenger(ids=user_id, idmes=message.message_id + 1)


class EventHandler(CallbackHandlers, MessageHandlers):
    """

    the initial message processing takes place in this class

    """

    def __init__(self, scripts_class_instance: dbscripts.Database, aiogram_bot: aiogram.Bot):

        if (type(scripts_class_instance) is not dbscripts.Database) or type(aiogram_bot) is not aiogram.Bot:
            raise TypeError('Not correct database assistant class or aiogram bot instance')

        self.database_operation_assistant = scripts_class_instance

        self.message_manager_ = message_manager.MessageManage(bot=aiogram_bot)

        self.bot_helper_scripts_ = helper_bot_scripts.HelperScripts(
            database_scripts=self.database_operation_assistant
        )

        self.callback_handler = callbacks.CallbackHandler(db_scripts=self.database_operation_assistant,
                                                          bot=aiogram_bot,
                                                          message_manager_=self.message_manager_,
                                                          bot_helper_scripts=self.bot_helper_scripts_)
