"""
Main file of _bot with handlers
"""
import asyncio

import aiogram

from src.prettybot.callback import callbacks
from src.prettybot.bot.messages import tgmessages, text_handlers
from src.prettybot.scripts import auxiliary
from src.prettybot.bot.db import database_assistant, registration_data_handler, large_messages

from src.prettybot.callback.callback_keyboards import *
from src.conf.recording_stages import *

__all__ = ['CallbackHandler', 'CommandHandler', 'ContentTypeHandler']


class BotEventHandler:
    database_operation_assistant: database_assistant.DatabaseScripts
    bot: aiogram.Bot
    message_sender: tgmessages.MessageSender
    message_deleter: tgmessages.MessageDeleter
    large_message_renderer: large_messages.LargeMessageRenderer
    large_message_generator: large_messages.LargeMessageTextGenerator
    registration_data_handler: registration_data_handler.RegistrationDataHandler

    def __init__(
            self,
            database_operation_assistant: database_assistant.DatabaseScripts,
            bot: aiogram.Bot,
            message_sender: tgmessages.MessageSender,
            message_deleter: tgmessages.MessageDeleter,
            large_message_renderer: large_messages.LargeMessageRenderer,
            large_message_generator: large_messages.LargeMessageTextGenerator,
            registration_data_handler_: registration_data_handler.RegistrationDataHandler):
        if not (type(database_operation_assistant) == database_assistant.DatabaseScripts
                and type(bot) == aiogram.Bot
                and type(message_sender) == tgmessages.MessageSender
                and type(message_deleter) == tgmessages.MessageDeleter
                and type(large_message_renderer) == large_messages.LargeMessageRenderer
                and type(large_message_generator) == large_messages.LargeMessageTextGenerator
                and type(registration_data_handler_) == registration_data_handler.RegistrationDataHandler):
            raise ValueError('Not correct type of given to __init__ arguments check type hints')

        self.database_operation_assistant = database_operation_assistant
        self.bot = bot
        self.message_sender = message_sender
        self.message_deleter = message_deleter
        self.large_message_renderer = large_message_renderer
        self.large_message_generator = large_message_generator
        self.registration_data_handler = registration_data_handler_


class CallbackHandler:
    database_operation_assistant: database_assistant.DatabaseScripts
    bot: aiogram.Bot
    message_sender: tgmessages.MessageSender
    large_message_renderer: large_messages.LargeMessageRenderer
    large_message_generator: large_messages.LargeMessageTextGenerator
    registration_data_handler: registration_data_handler.RegistrationDataHandler

    def __init__(self, bot_event_handler: BotEventHandler):
        self.__dict__ = {param: bot_event_handler.__dict__[param]
                         for param in bot_event_handler.__dict__
                         if param in CallbackHandler.__annotations__}

    async def inline_keyboard_callback(self, callback_query: aiogram.types.CallbackQuery):
        sending_response = None
        user_id, query_id, from_message_id = (callback_query.from_user.id,
                                              callback_query.id,
                                              callback_query.message.message_id)

        payload = callbacks.unpack_playload(payload_string=callback_query.data)
        type_request, type_requested_operation = payload.values()

        user_lang_code = self.database_operation_assistant.get_user_lang_code(user_id=user_id)
        _, type_logging, stage_logging = self.database_operation_assistant.get_logging_info(user_id=user_id).object

        await self.bot.answer_callback_query(query_id)

        if type_request == 'main':
            if type_requested_operation == 'change_profile_data':
                await self.bot.edit_message_reply_markup(chat_id=user_id,
                                                         message_id=from_message_id,
                                                         reply_markup=INLINE_CHANGE_PROF_DATA_KB[user_lang_code])

            elif type_requested_operation == 'start_find':
                sending_response = await self.large_message_renderer.render_finding_message(user_id=user_id,
                                                                                            user_lang_code=user_lang_code)

                await self.large_message_renderer.delete_large_message(user_id=user_id,
                                                                       type_message=PROFILE_MESSAGE_TYPE)

            elif type_requested_operation == 'back':
                await self.large_message_renderer.render_profile(
                    account_body=self.large_message_generator.generate_profile_body(
                        user_id=user_id,
                        user_lang_code=user_lang_code
                    ),
                    user_id=user_id,
                    user_lang_code=user_lang_code)

                await self.large_message_renderer.delete_large_message(user_id=user_id,
                                                                       type_message=QUESTION_MESSAGE_TYPE)

        elif type_request in ('change', 'changewish'):
            if type_requested_operation != 'back':

                callback_markup = callbacks.get_inline_keyboard_by_stage(
                    stage=STAGE_BY_PAYLOAD[type_requested_operation],
                )

                if type_request == 'change':
                    sending_response = await self.message_sender.send(
                        user_id=user_id,
                        description=QUESTION_STATEMENT_BY_CALLBACK_PAYLOAD[
                            type_requested_operation
                        ][user_lang_code],
                        markup=callback_markup[user_lang_code]
                    )

                elif type_request == 'changewish':
                    sending_response = await self.message_sender.send(
                        user_id=user_id,
                        description=QUESTION_STATEMENT_BY_CALLBACK_PAYLOAD_FINDING[
                            type_requested_operation
                        ][user_lang_code],
                        markup=callback_markup[user_lang_code]
                    )

                await self.large_message_renderer.delete_large_message(user_id=user_id,
                                                                       type_message=QUESTION_MESSAGE_TYPE)

            elif type_requested_operation == 'back':
                await self.bot.edit_message_reply_markup(chat_id=user_id,
                                                         message_id=from_message_id,
                                                         reply_markup=INLINE_PROFILE_KB[user_lang_code])

            if type_requested_operation in STAGE_BY_PAYLOAD.keys():
                stage = STAGE_BY_PAYLOAD[payload.get('type_requested_operation')]

                self.database_operation_assistant.change_state_logging(user_id=user_id,
                                                                       logtype=STAGES_RECORDING[1]
                                                                       if type_request == 'change' else
                                                                       STAGES_RECORDING[2],
                                                                       logstage=stage
                                                                       )

        elif type_request == 'sex':
            if not stage_logging:
                return

            received_sex = auxiliary.convert_sex_type(type_requested_operation)

            self.registration_data_handler.record_registration_data(
                user_id=user_id,
                message_text=received_sex,
                logstage=stage_logging,
                logtype=type_logging
            )

            if type_logging == TYPE_RECORDING[0]:
                sending_response = await self.message_sender.send(
                    user_id=user_id,
                    description=STATEMENTS_BY_LANG[
                        user_lang_code
                    ].q_desc
                )

                self.database_operation_assistant.change_state_logging(
                    user_id=user_id,
                    logtype=type_logging,
                    logstage=auxiliary.increase_stage_recording(stage_logging))

            elif type_logging == TYPE_RECORDING[2]:
                sending_response = await self.large_message_renderer.render_finding_message(
                    user_id=user_id,
                    user_lang_code=user_lang_code)

            self.database_operation_assistant.add_main_message_to_db(
                user_id=user_id,
                id_message=sending_response.object,
                type_message=QUESTION_MESSAGE_TYPE)

            await self.large_message_renderer.delete_large_message(
                user_id=user_id,
                type_message=QUESTION_MESSAGE_TYPE)

        elif type_request == 'find':

            if type_requested_operation.split('&')[0] == 'start':
                searching_mode = type_requested_operation.split('&')[1]
                finded_users_ids = []

                if searching_mode == 'spec':
                    searching_settings = self.database_operation_assistant.get_user_wishes(user_id=user_id).object
                    print(searching_settings, '_search_settings- ')
                    finded_users_ids = self.database_operation_assistant.get_users_ids_by_params(user_id=user_id)

                elif searching_mode == 'fast':
                    finded_users_ids = self.database_operation_assistant.get_users_ids_by_params(user_id=user_id)

                if finded_users_ids.object:
                    sending_response = await self.message_sender.send(
                        user_id=user_id,
                        description=STATEMENTS_BY_LANG[user_lang_code].find_successful
                    )

                    #  MESSAGE TO SECOND USER

                    result_second_user_message_id = await self.message_sender.send(
                        user_id=user_id,
                        description=STATEMENTS_BY_LANG[user_lang_code]
                    )

                    # self.database_operation_assistant.del_user_from_buffer(user_id=finded_users_ids.object)

                    # self.database_operation_assistant.add_main_message_to_db(user_id=finded_users_ids.object,
                    #                                                           id_message=result_second_user_message_id,
                    #                                                           type_message=QUESTION_MESSAGE_TYPE)

                    # self.database_operation_assistant.change_chatting_condition(user_id=finded_users_ids.object,
                    #                                                              new_condition=True)

                    self.database_operation_assistant.change_chatting_condition(user_id=user_id,
                                                                                new_condition=True)

                elif not finded_users_ids.object:
                    if searching_mode == 'spec':
                        sending_response = await self.message_sender.send(
                            user_id=user_id,
                            description=STATEMENTS_BY_LANG[user_lang_code].not_spec_users_warn
                        )

                    elif searching_mode == 'fast':
                        sending_response = await self.message_sender.send(
                            user_id=user_id,
                            description=STATEMENTS_BY_LANG[user_lang_code].not_spec_users_warn
                        )

            elif type_requested_operation == 'clarify':
                sending_response = await self.message_sender.send(
                    user_id=user_id,
                    description=self.large_message_renderer.get_finding_params(
                        user_id=user_id,
                        user_lang_code=user_lang_code
                    ),
                    markup=INLINE_CHANGE_PARAMS_FIND_KB[
                        user_lang_code])

            elif type_requested_operation == 'back':
                id_finding_window = await self.large_message_renderer.render_finding_message(
                    user_id=user_id,
                    user_lang_code=user_lang_code)
                await self.large_message_renderer.delete_large_message(
                    user_id=user_id,
                    type_message=QUESTION_MESSAGE_TYPE)

                self.database_operation_assistant.add_main_message_to_db(
                    user_id=user_id,
                    id_message=id_finding_window.object,
                    type_message=QUESTION_MESSAGE_TYPE)

                return

            await self.large_message_renderer.delete_large_message(user_id=user_id, type_message=QUESTION_MESSAGE_TYPE)

        if sending_response and sending_response.object:
            self.database_operation_assistant.add_main_message_to_db(user_id=user_id,
                                                                     id_message=sending_response.object,
                                                                     type_message=QUESTION_MESSAGE_TYPE)


class CommandHandler:
    database_operation_assistant: database_assistant.DatabaseScripts
    message_sender: tgmessages.MessageSender
    message_deleter: tgmessages.MessageDeleter
    large_message_renderer: large_messages.LargeMessageRenderer
    large_message_generator: large_messages.LargeMessageTextGenerator
    registration_data_handler: registration_data_handler.RegistrationDataHandler

    def __init__(self, bot_event_handler: BotEventHandler):
        self.__dict__ = {param: bot_event_handler.__dict__[param]
                         for param in bot_event_handler.__dict__
                         if param in CommandHandler.__annotations__}

    async def start(self, message: aiogram.types.Message, user_id: int):
        user_logging_condition = self.database_operation_assistant.get_logging_info(user_id=user_id)

        if not user_logging_condition.status:
            await self.message_sender.send_except_message(user_id=user_id)
            return

        if not user_logging_condition.object:
            response = self.database_operation_assistant.add_user_entry(user_id=user_id,
                                                                        fname=message.from_user.first_name,
                                                                        lname=message.from_user.last_name,
                                                                        telegname=message.chat.username,
                                                                        date_message=message.date
                                                                        )

            if not response.status:
                await self.message_sender.send_except_message(user_id=user_id)
                return

            welcome_sending_response = await self.message_sender.send(user_id=user_id,
                                                                      description=BASE_STATEMENTS.welcome.format(
                                                                          message.from_user.first_name)
                                                                      )

            entry_sending_response = await self.message_sender.send(user_id=user_id,
                                                                    description=STATEMENTS_BY_LANG[
                                                                        DEFAULT_LANG
                                                                    ].entry_registration
                                                                    )

            await self.message_deleter.delete_message(user_id=user_id,
                                                      idmes=message.message_id,
                                                      )

            self.database_operation_assistant.add_main_message_to_db(user_id=user_id,
                                                                     id_message=welcome_sending_response.object,
                                                                     type_message=START_MESSAGE_TYPE)

            self.database_operation_assistant.add_main_message_to_db(user_id=user_id,
                                                                     id_message=entry_sending_response.object,
                                                                     type_message=QUESTION_MESSAGE_TYPE)

        elif user_logging_condition.object:
            user_lang_code = self.database_operation_assistant.get_user_lang_code(user_id=user_id)

            logging, logging_type, logging_stage = user_logging_condition.object

            if logging:
                if logging_type not in MAIN_REGISTRATION_TYPE:
                    self.database_operation_assistant.change_state_logging(user_id=user_id, stop_logging=True)

                    for type_ in TYPES_MAIN_MESSAGES:
                        if type_ != PROFILE_MESSAGE_TYPE:
                            await self.large_message_renderer.delete_large_message(user_id=user_id, type_message=type_)

                    await self.large_message_renderer.render_profile(
                        account_body=self.large_message_generator.generate_profile_body(
                            user_id=user_id,
                            user_lang_code=user_lang_code
                        ),
                        user_id=user_id,
                        user_lang_code=user_lang_code)

                    await self.message_deleter.delete_message(user_id=user_id, idmes=message.message_id)

                else:
                    sending_response = await self.message_sender.send(user_id=user_id,
                                                                      description=STATEMENTS_BY_LANG[
                                                                          user_lang_code].help)

                    await self.message_deleter.delete_message(user_id=user_id, idmes=message.message_id)
                    await auxiliary.start_delay(LONG_DELAY)
                    await self.message_deleter.delete_message(user_id=user_id, idmes=sending_response.object)

            elif not logging:
                await self.large_message_renderer.render_profile(
                    account_body=self.large_message_generator.generate_profile_body(
                        user_id=user_id,
                        user_lang_code=user_lang_code
                    ),
                    user_id=user_id,
                    user_lang_code=user_lang_code)
                await self.message_deleter.delete_message(user_id=user_id, idmes=message.message_id)

            else:
                sending_response = await self.message_sender.send(user_id=user_id,
                                                                  description=STATEMENTS_BY_LANG[user_lang_code].help)

                await self.message_deleter.delete_message(user_id=user_id, idmes=message.message_id)
                await auxiliary.start_delay(LONG_DELAY)
                await self.message_deleter.delete_message(user_id=user_id, idmes=sending_response.object)

    async def help(self, message: aiogram.types.Message, user_id: int):
        user_lang_code = self.database_operation_assistant.get_user_lang_code(user_id=user_id)

        sending_response = await self.message_sender.send(
            user_id=user_id,
            description=STATEMENTS_BY_LANG[user_lang_code].help
        )

        await self.message_deleter.delete_message(user_id=user_id, idmes=message.message_id)

        await auxiliary.start_delay(MEDIUM_DELAY)

        await self.message_deleter.delete_message(user_id=user_id,
                                                  idmes=sending_response.object)

    async def restart(self, message: aiogram.types.Message, user_id: int):

        delete_tasks = list()

        for type_main_message in TYPES_MAIN_MESSAGES:
            delete_tasks.append(asyncio.create_task(self.large_message_renderer.delete_large_message(
                user_id=user_id,
                type_message=type_main_message)
            ))

        await asyncio.gather(*delete_tasks)

        self.database_operation_assistant.del_user_annotations(user_id=user_id)
        await self.message_deleter.delete_message(user_id=user_id, idmes=message.message_id)

    async def change_lang(self, message: aiogram.types.Message, user_id: int):

        self.database_operation_assistant.change_user_lang(user_id=user_id, lang_code=message.text[1:3])

        await self.message_sender.send(
            user_id=user_id,
            description=STATEMENTS_BY_LANG[
                self.database_operation_assistant.get_user_lang_code(user_id=user_id)
            ].change_lang_good)

        await self.message_deleter.delete_message(user_id=user_id, idmes=message.message_id)

        await auxiliary.start_delay(delay=DEFAULT_DELAY)

        await self.message_deleter.delete_message(user_id=user_id, idmes=message.message_id + 1)

    async def stop_chatting(self, message: aiogram.types.Message, user_id: int):

        current_chatting_condition = self.database_operation_assistant.get_chatting_condition(user_id=user_id)

        if current_chatting_condition.object:
            user_lang_code = self.database_operation_assistant.get_user_lang_code(user_id=user_id)

            self.database_operation_assistant.change_chatting_condition(user_id=user_id, new_condition=False)

            response_sending = await self.message_sender.send(user_id=user_id,
                                                              description=STATEMENTS_BY_LANG[
                                                                  user_lang_code].end_chatting)

            await self.large_message_renderer.render_profile(
                account_body=self.large_message_generator.generate_profile_body(
                    user_id=user_id,
                    user_lang_code=user_lang_code),

                user_id=user_id,
                user_lang_code=user_lang_code)

            await auxiliary.start_delay(DEFAULT_DELAY)
            await self.message_deleter.delete_message(user_id=user_id, idmes=response_sending.object)

        await self.message_deleter.delete_message(user_id=user_id, idmes=message.message_id)


class ContentTypeHandler:
    database_operation_assistant: database_assistant.DatabaseScripts
    message_sender: tgmessages.MessageSender
    message_deleter: tgmessages.MessageDeleter
    large_message_renderer: large_messages.LargeMessageRenderer
    large_message_generator: large_messages.LargeMessageTextGenerator
    registration_data_handler: registration_data_handler.RegistrationDataHandler

    def __init__(self, bot_event_handler: BotEventHandler):
        self.__dict__ = {param: bot_event_handler.__dict__[param]
                         for param in bot_event_handler.__dict__
                         if param in ContentTypeHandler.__annotations__}

    async def photo(self, message: aiogram.types.Message, user_id: int) -> None:

        logging, type_logging, stage_logging = self.database_operation_assistant.get_logging_info(
            user_id=user_id
        ).object

        file_id = message.photo[0]['file_id']

        print(logging, stage_logging, '-p-----------------')

        if logging and stage_logging == STAGES_RECORDING[4]:
            user_lang_code = self.database_operation_assistant.get_user_lang_code(user_id=user_id)

            statement_response = text_handlers.handle_message(
                file_id,
                user_lang_code,
                type_logging,
                self.database_operation_assistant.all_cities,
                recordstage=stage_logging
            )

            if statement_response.status:
                self.registration_data_handler.record_registration_data(user_id=user_id,
                                                                        message_text=file_id,
                                                                        logstage=stage_logging,
                                                                        logtype=type_logging,
                                                                        updating_data=
                                                                        True if type_logging == TYPE_RECORDING[1]
                                                                        else False)

                await self.large_message_renderer.render_profile(
                    account_body=self.large_message_generator.generate_profile_body(
                        user_id=user_id,
                        user_lang_code=user_lang_code
                    ),
                    user_id=user_id,
                    user_lang_code=user_lang_code,
                )

                self.database_operation_assistant.change_state_logging(user_id=user_id, stop_logging=True)

            await self.large_message_renderer.delete_large_message(user_id=user_id,
                                                                   type_message=QUESTION_MESSAGE_TYPE)

        await self.message_deleter.delete_message(user_id=message.from_user.id,
                                                  idmes=message.message_id)

    async def text(self, message: aiogram.types.Message, user_id: int) -> None:

        if self.database_operation_assistant.get_chatting_condition(user_id=user_id).object:
            await self.message_sender.send(user_id=message.from_user.id,
                                           description=message.text)

            return

        user_logging_data = self.database_operation_assistant.get_logging_info(user_id=user_id)

        if not user_logging_data.status or len(user_logging_data.object) < 3:
            await self.message_sender.send_except_message(user_id=user_id)
            return

        if not user_logging_data.object:
            await self.message_sender.send_except_message(user_id=user_id,
                                                          description=STATEMENTS_BY_LANG[DEFAULT_LANG].start_warn)

            return

        logging, type_logging, stage_logging = user_logging_data.object
        sending_response = None

        if logging:
            user_lang_code = self.database_operation_assistant.get_user_lang_code(user_id=user_id)

            statement = text_handlers.handle_message(message.text,
                                                     user_lang_code,
                                                     type_logging,
                                                     self.database_operation_assistant.all_cities,
                                                     recordstage=stage_logging)

            if stage_logging in STAGE_BLOCKED_TEXT_MESSAGES:
                if stage_logging == STAGES_RECORDING[2]:
                    sending_response = await self.message_sender.send(
                        user_id=user_id,
                        description=STATEMENT_FOR_STAGE[stage_logging],
                        markup=callbacks.get_inline_keyboard_by_stage(stage=stage_logging)
                    )

            if statement.status:
                self.registration_data_handler.record_registration_data(user_id=user_id,
                                                                        message_text=message.text,
                                                                        logstage=stage_logging,
                                                                        logtype=type_logging)

                if type_logging == TYPE_RECORDING[0]:

                    markup_for_stage = callbacks.get_inline_keyboard_by_stage(stage=stage_logging)

                    if statement.object:
                        if stage_logging:
                            if type(markup_for_stage) is dict:
                                sending_response = await self.message_sender.send(
                                    user_id=user_id,
                                    description=statement.object,
                                    markup=markup_for_stage[user_lang_code]
                                )

                            else:
                                sending_response = await self.message_sender.send(
                                    user_id=user_id,
                                    description=statement.object
                                )

                            self.database_operation_assistant.change_state_logging(
                                user_id=user_id,
                                logtype=type_logging,
                                logstage=auxiliary.increase_stage_recording(stage_logging))

                if type_logging == TYPE_RECORDING[1]:
                    await self.large_message_renderer.render_profile(
                        account_body=self.large_message_generator.generate_profile_body(
                            user_id=user_id,
                            user_lang_code=user_lang_code
                        ),
                        user_id=user_id,
                        user_lang_code=user_lang_code)

                    self.database_operation_assistant.change_state_logging(user_id=user_id, stop_logging=True)

                if type_logging == TYPE_RECORDING[2]:
                    sending_response = await self.large_message_renderer.render_finding_message(
                        user_id=user_id,
                        user_lang_code=user_lang_code)

            else:
                if statement.object:
                    sending_response = await self.message_sender.send_except_message(user_id=user_id,
                                                                                     user_lang_code=user_lang_code,
                                                                                     description=statement.object)

            await self.large_message_renderer.delete_large_message(user_id=user_id,
                                                                   type_message=QUESTION_MESSAGE_TYPE)

            if sending_response and sending_response.status:
                self.database_operation_assistant.add_main_message_to_db(user_id=user_id,
                                                                         id_message=sending_response.object,
                                                                         type_message=QUESTION_MESSAGE_TYPE)

        await self.message_deleter.delete_message(user_id=user_id,
                                                  idmes=message.message_id)
