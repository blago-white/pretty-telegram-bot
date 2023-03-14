import aiogram

from src.prettybot.bot.messages import chat_interaction
from src.prettybot.bot.minorscripts import supportive
from src.prettybot.bot.dbassistant import database_assistant
from src.prettybot.bot.dbassistant.registrations import registration_data_handler
from src.prettybot.bot.messages.botmessages import botmessages
from src.prettybot.bot.messages.handlers.eventhandlers import event_handler

from src.prettybot.bot.callback.callback_keyboards import *
from src.config.recording_stages import *


class CallbackHandler:
    database_operation_assistant: database_assistant.Database
    bot: aiogram.Bot
    message_sender: chat_interaction.MessageSender
    large_message_renderer: botmessages.MainMessagesRenderer
    registration_data_handler: registration_data_handler.RegistrationParamsHandler

    def __init__(self, bot_event_handler: event_handler.BotEventHandler):
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
                    recordtype=TYPE_RECORDING[0 if type_request == 'change' else 2]
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
                    record_type=TYPE_RECORDING[1]
                    if type_request == 'change' else
                    TYPE_RECORDING[2],
                    record_stage=STAGE_BY_PAYLOAD[payload.get('type_requested_operation')]
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

            self.database_operation_assistant.increase_recording_stage(user_id=user_id)

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

