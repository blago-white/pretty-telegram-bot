"""
Main file of _bot with handlers
"""

import aiogram

from src.prettybot.bot.messages import chat_interaction
from src.prettybot.bot.messages.handlers import user_answer_handlers
from src.prettybot.bot.minorscripts import supportive
from src.prettybot.bot.db import database_assistant
from src.prettybot.bot.db.registration import registration_data_handler
from src.prettybot.bot.messages.botmessages import botmessages
from src.prettybot.bot.asyncioscripts import coroutine_executor

from src.prettybot.bot.callback.callback_keyboards import *
from src.config.recording_stages import *


class BotEventHandler:
    database_operation_assistant: database_assistant.Database
    bot: aiogram.Bot
    message_sender: chat_interaction.MessageSender
    message_deleter: chat_interaction.MessageDeleter
    large_message_renderer: botmessages.MainMessagesRenderer
    registration_data_handler: registration_data_handler.RegistrationParamsHandler

    def __init__(
            self,
            database_operation_assistant: database_assistant.Database,
            bot: aiogram.Bot,
            message_sender: chat_interaction.MessageSender,
            message_deleter: chat_interaction.MessageDeleter,
            large_message_renderer: botmessages.MainMessagesRenderer,
            registration_data_handler_: registration_data_handler.RegistrationParamsHandler):
        if not (type(database_operation_assistant) == database_assistant.Database
                and type(bot) == aiogram.Bot
                and type(message_sender) == chat_interaction.MessageSender
                and type(message_deleter) == chat_interaction.MessageDeleter
                and type(large_message_renderer) == botmessages.MainMessagesRenderer
                and type(registration_data_handler_) == registration_data_handler.RegistrationParamsHandler):
            raise ValueError('Not correct type of given to __init__ arguments check type hints')

        self.database_operation_assistant = database_operation_assistant
        self.bot = bot
        self.message_sender = message_sender
        self.message_deleter = message_deleter
        self.large_message_renderer = large_message_renderer
        self.registration_data_handler = registration_data_handler_


class CallbackHandler:
    database_operation_assistant: database_assistant.Database
    bot: aiogram.Bot
    message_sender: chat_interaction.MessageSender
    large_message_renderer: botmessages.MainMessagesRenderer
    registration_data_handler: registration_data_handler.RegistrationParamsHandler

    def __init__(self, bot_event_handler: BotEventHandler):
        self.__dict__ = {param: bot_event_handler.__dict__[param]
                         for param in bot_event_handler.__dict__
                         if param in CallbackHandler.__annotations__}

    async def handle_callback(self, callback_query: aiogram.types.CallbackQuery):
        user_id, query_id, from_message_id = (callback_query.from_user.id,
                                              callback_query.id,
                                              callback_query.message.message_id)

        payload = supportive.unpack_playload(payload_string=callback_query.data)
        type_request, type_requested_operation = payload.values()

        user_lang_code = self.database_operation_assistant.get_user_lang_code(user_id=user_id)

        _, type_logging, stage_logging = self.database_operation_assistant.get_recording_condition(
            user_id=user_id
        ).object

        await self.bot.answer_callback_query(query_id)

        if type_request == 'main':
            if type_requested_operation == 'change_profile_data':
                await self.bot.edit_message_reply_markup(chat_id=user_id,
                                                         message_id=from_message_id,
                                                         reply_markup=INLINE_CHANGE_PROF_DATA_KB[user_lang_code])

            elif type_requested_operation == 'start_find':
                await self.large_message_renderer.render_finding_message(user_id=user_id,
                                                                         user_lang_code=user_lang_code)

            elif type_requested_operation == 'back':
                await self.large_message_renderer.render_profile(
                    user_id=user_id,
                    user_lang_code=user_lang_code)

        elif type_request in ('change', 'changewish'):
            if type_requested_operation != 'back':

                callback_markup = supportive.get_inline_keyboard_by_stage(
                    recordstage=STAGE_BY_PAYLOAD[type_requested_operation],
                    recordtype=type_logging
                )

                await self.large_message_renderer.render_main_message(
                    user_id=user_id,
                    description=(QUESTION_STATEMENT_BY_CALLBACK_PAYLOAD
                                 if type_request == 'change' else
                                 QUESTION_STATEMENT_BY_CALLBACK_PAYLOAD_FINDING
                                 )[
                        type_requested_operation][user_lang_code],
                    markup=callback_markup[user_lang_code]
                )

            elif type_requested_operation == 'back':
                await self.bot.edit_message_reply_markup(chat_id=user_id,
                                                         message_id=from_message_id,
                                                         reply_markup=INLINE_PROFILE_KB[user_lang_code])

            if type_requested_operation in STAGE_BY_PAYLOAD.keys():
                self.database_operation_assistant.start_recording(
                    user_id=user_id,
                    logtype=TYPE_RECORDING[1]
                    if type_request == 'change' else
                    TYPE_RECORDING[2],
                    logstage=STAGE_BY_PAYLOAD[payload.get('type_requested_operation')]
                )

        elif type_request == 'sex':
            self.registration_data_handler.record_user_param(
                user_id=user_id,
                message_payload=type_requested_operation,
                record_stage=stage_logging,
                record_type=type_logging
            )

            if type_logging == TYPE_RECORDING[0]:
                await self.large_message_renderer.render_main_message(
                    user_id=user_id,
                    description=STATEMENTS_BY_LANG[user_lang_code].q_desc
                )

            elif type_logging == TYPE_RECORDING[2]:
                await self.large_message_renderer.render_finding_message(
                    user_id=user_id,
                    user_lang_code=user_lang_code)

            self.database_operation_assistant.increase_recording_stage(
                user_id=user_id,
                logtype=type_logging,
                logstage=stage_logging)

        elif type_request == 'find':
            if type_requested_operation.split('&')[0] == 'start':
                searching_mode = type_requested_operation.split('&')[1]
                finded_users_ids = []

                if searching_mode == 'spec':
                    searching_settings = self.database_operation_assistant.get_user_wishes(user_id=user_id).object
                    finded_users_ids = self.database_operation_assistant.get_users_ids_by_params(user_id=user_id)

                elif searching_mode == 'fast':
                    finded_users_ids = self.database_operation_assistant.get_users_ids_by_params(user_id=user_id)

                if finded_users_ids.object:
                    await self.large_message_renderer.render_main_message(
                        user_id=user_id,
                        description=STATEMENTS_BY_LANG[user_lang_code].find_successful)

                    #  MESSAGE TO SECOND USER

                    # await self.large_message_renderer.render_main_message(
                    #         user_id=user_id,
                    #         description=STATEMENTS_BY_LANG[user_lang_code])

                    # self.database_operation_assistant.del_user_from_buffer(user_id=finded_users_ids.object)

                    # self.database_operation_assistant.add_main_message_to_db(user_id=finded_users_ids.object,
                    #                                                           id_message=result_second_user_message_id,
                    #                                                           type_message=QUESTION_MESSAGE_TYPE)

                    # self.database_operation_assistant.change_chatting_condition(user_id=finded_users_ids.object,
                    #                                                              new_condition=True)

                    self.database_operation_assistant.start_chatting(user_id=user_id)

                elif not finded_users_ids.object:
                    await self.large_message_renderer.render_main_message(
                        user_id=user_id,
                        description=STATEMENTS_BY_LANG[user_lang_code].not_spec_users_warn)

            elif type_requested_operation == 'clarify':
                await self.large_message_renderer.render_clarify_message(user_id=user_id,
                                                                         user_lang_code=user_lang_code)

            elif type_requested_operation == 'back':
                await self.large_message_renderer.render_finding_message(
                    user_id=user_id,
                    user_lang_code=user_lang_code)


class CommandsHandler:
    database_operation_assistant: database_assistant.Database
    message_sender: chat_interaction.MessageSender
    message_deleter: chat_interaction.MessageDeleter
    large_message_renderer: botmessages.MainMessagesRenderer
    registration_data_handler: registration_data_handler.RegistrationParamsHandler

    def __init__(self, bot_event_handler: BotEventHandler):
        self.__dict__ = {param: bot_event_handler.__dict__[param]
                         for param in bot_event_handler.__dict__
                         if param in CommandsHandler.__annotations__}

    async def handle_start(self, message: aiogram.types.Message, user_id: int, user_lang_code: str):
        user_logging_condition = self.database_operation_assistant.get_recording_condition(user_id=user_id)
        if user_logging_condition.object:
            logging, logging_type, logging_stage = user_logging_condition.object

            if logging:
                if logging_type in MAIN_REGISTRATION_TYPE:
                    await self.large_message_renderer.render_disappearing_message(
                        user_id=user_id,
                        retrievable_message_id=message.message_id,
                        description=STATEMENTS_BY_LANG[user_lang_code].help,
                        delay_before_deleting=LONG_DELAY
                    )

                else:
                    self.database_operation_assistant.stop_recording(user_id=user_id)
                    await self.large_message_renderer.render_profile(user_id=user_id, user_lang_code=user_lang_code)

            else:
                await self.large_message_renderer.render_profile(user_id=user_id, user_lang_code=user_lang_code)

        else:
            self.database_operation_assistant.add_new_user(user_id=user_id,
                                                           fname=message.from_user.first_name,
                                                           lname=message.from_user.last_name,
                                                           telegname=message.chat.username,
                                                           date_message=message.date
                                                           )

            await self.large_message_renderer.render_main_message(
                user_id=user_id,
                description=BASE_STATEMENTS.welcome.format(message.from_user.first_name))

    async def handle_help(self, message: aiogram.types.Message, user_id: int, user_lang_code: str):
        await self.large_message_renderer.render_disappearing_message(
            user_id=user_id,
            retrievable_message_id=message.message_id,
            description=STATEMENTS_BY_LANG[user_lang_code].help,
            delay_before_deleting=MEDIUM_DELAY)

    async def handle_restart(self, *args):
        await self.large_message_renderer.delete_main_message(user_id=args[1])
        self.database_operation_assistant.delete_user_records(user_id=args[1])

    async def handle_change_lang(self, message: aiogram.types.Message, user_id: int, _: str):
        self.database_operation_assistant.change_user_lang(user_id=user_id, lang_code=message.text[1:3])
        await self.large_message_renderer.render_disappearing_message(
            user_id=user_id,
            retrievable_message_id=message.message_id,
            description=STATEMENTS_BY_LANG[message.text[1:3]].change_lang_good,
            delay_before_deleting=DEFAULT_DELAY
        )

    async def handle_stop_chatting(self, message: aiogram.types.Message, user_id: int, user_lang_code: str):
        if self.database_operation_assistant.get_chatting_condition(user_id=user_id).object:
            self.database_operation_assistant.stop_chatting(user_id=user_id)
            await coroutine_executor.execute_coros(
                self.large_message_renderer.render_profile(
                    user_id=user_id,
                    user_lang_code=user_lang_code),
                self.large_message_renderer.render_disappearing_message(
                    user_id=user_id,
                    retrievable_message_id=message.message_id,
                    description=STATEMENTS_BY_LANG[user_lang_code].end_chatting,
                    delay_before_deleting=DEFAULT_DELAY
                ))


class ContentTypesHandler:
    database_operation_assistant: database_assistant.Database
    message_sender: chat_interaction.MessageSender
    message_deleter: chat_interaction.MessageDeleter
    large_message_renderer: botmessages.MainMessagesRenderer
    registration_data_handler: registration_data_handler.RegistrationParamsHandler

    def __init__(self, bot_event_handler: BotEventHandler):
        self.__dict__ = {param: bot_event_handler.__dict__[param]
                         for param in bot_event_handler.__dict__
                         if param in ContentTypesHandler.__annotations__}

    async def handle_photo(self, message: aiogram.types.Message, user_id: int, user_lang_code: str) -> None:
        logging, type_logging, stage_logging = self.database_operation_assistant.get_recording_condition(
            user_id=user_id
        ).object

        file_id = message.photo[0]['file_id']

        if logging and stage_logging == STAGES_RECORDING[4]:
            self.registration_data_handler.record_user_param(
                user_id=user_id,
                message_payload=file_id,
                record_stage=stage_logging,
                record_type=type_logging)

            await self.large_message_renderer.render_profile(
                user_id=user_id,
                user_lang_code=user_lang_code,
            )

            self.database_operation_assistant.stop_recording(user_id=user_id)

    async def handle_text(self, message: aiogram.types.Message, user_id: int, user_lang_code: str) -> None:
        if self.database_operation_assistant.get_chatting_condition(user_id=user_id).object:
            """in future on this place be methods to re-send message to friend of user"""

            await self.message_sender.send(user_id=message.from_user.id,
                                           description=message.text)

            return

        user_logging_data = self.database_operation_assistant.get_recording_condition(user_id=user_id)

        if not user_logging_data.object:
            await self.large_message_renderer.render_main_message(
                user_id=user_id,
                description=STATEMENTS_BY_LANG[DEFAULT_LANG].start_warn,
                with_warn=True)

            return

        logging, type_logging, stage_logging = user_logging_data.object

        if logging:
            if stage_logging in STAGE_BLOCKED_TEXT_MESSAGES and stage_logging == STAGES_RECORDING[2]:
                markup = supportive.get_inline_keyboard_by_stage(recordstage=stage_logging, recordtype=type_logging)
                await self.large_message_renderer.render_main_message(
                    user_id=user_id,
                    description=STATEMENTS_BY_LANG[user_lang_code].q_find_sex,
                    markup=markup[user_lang_code])

                return

            statement = user_answer_handlers.handle_message(message.text,
                                                            user_lang_code,
                                                            type_logging,
                                                            self.database_operation_assistant.all_cities,
                                                            recordstage=stage_logging)

            if statement.status:
                self.registration_data_handler.record_user_param(user_id=user_id,
                                                                 message_payload=message.text,
                                                                 record_stage=stage_logging,
                                                                 record_type=type_logging)

                if type_logging == TYPE_RECORDING[0] and stage_logging:
                    markup_for_stage = supportive.get_inline_keyboard_by_stage(
                        recordstage=stage_logging,
                        recordtype=type_logging)

                    await self.large_message_renderer.render_main_message(
                        user_id=user_id,
                        description=statement.object,
                        markup=markup_for_stage[user_lang_code]
                    )

                    self.database_operation_assistant.increase_recording_stage(
                        user_id=user_id,
                        logtype=type_logging,
                        logstage=stage_logging)

                elif type_logging == TYPE_RECORDING[1]:
                    await self.large_message_renderer.render_profile(
                        user_id=user_id,
                        user_lang_code=user_lang_code)

                    self.database_operation_assistant.stop_recording(user_id=user_id)

                elif type_logging == TYPE_RECORDING[2]:
                    await self.large_message_renderer.render_finding_message(
                        user_id=user_id,
                        user_lang_code=user_lang_code)

            elif not statement.status and statement.object:
                await self.large_message_renderer.render_main_message(
                    user_id=user_id,
                    description=statement.object,
                    with_warn=True
                )
