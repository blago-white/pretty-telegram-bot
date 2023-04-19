import aiogram
import inspect
from typing import Callable, Union, Any

from ...botmessages import botmessages

from src.prettybot.bot import _lightscripts
from src.prettybot.bot.dbassistant import database_assistant
from src.prettybot.bot.dbassistant.registrations.registration_data_handler import RegistrationParamsHandler
from src.prettybot.exceptions import exceptions_inspector

from src.prettybot.bot.callback.callback_keyboards import *
from src.config.recording_stages import *

__all__ = ['CallbackHandler']


class CallbackHandler:
    _HANDLING_CALLBACK_ERROR_MESSAGE_TO_USER = 'error on server'
    _ACCOUNT_DATA_CHANGING_PREFIX = 'change'
    _FINDING_SETTINGS_CHANGING_PREFIX = 'changewish'

    def __init__(
            self, database_operation_assistant: database_assistant.BotDatabase,
            bot: aiogram.Bot,
            large_message_renderer: botmessages.MainMessagesRenderer,
            registration_data_handler: RegistrationParamsHandler
    ) -> None:
        self._database_operation_assistant = database_operation_assistant
        self._bot = bot
        self._large_message_renderer = large_message_renderer
        self._registration_data_handler = registration_data_handler

    async def handle_profile_calls(self, callback_query: aiogram.types.CallbackQuery, callback_data: dict):
        type_requested_operation = callback_data['called_operation']
        user_id = callback_query.from_user.id
        from_message_id = callback_query.message.message_id
        user_lang_code = self._database_operation_assistant.get_user_lang_or_default(user_id=user_id)

        if type_requested_operation == 'change_profile_data':
            await self._bot.edit_message_reply_markup(chat_id=user_id,
                                                      message_id=from_message_id,
                                                      reply_markup=INLINE_CHANGE_PROF_DATA_KB[user_lang_code])

        elif type_requested_operation == 'start_find':
            await self._large_message_renderer.render_finding_message(user_id=user_id,
                                                                      user_lang_code=user_lang_code)

        elif type_requested_operation == 'back':
            await self._large_message_renderer.render_profile(
                user_id=user_id,
                user_lang_code=user_lang_code)

    async def handle_change_calls(self, callback_query: aiogram.types.CallbackQuery, callback_data: dict):
        type_requested_operation = callback_data['called_operation']
        type_request = callback_data['@']
        user_id = callback_query.from_user.id
        user_lang_code = self._database_operation_assistant.get_user_lang_or_default(user_id=user_id)

        if type_requested_operation == 'back':
            await self._bot.edit_message_reply_markup(
                chat_id=user_id,
                message_id=callback_query.message.message_id,
                reply_markup=INLINE_PROFILE_KB[user_lang_code]
            )
            return

        type_recording, stage_recording = (
            TYPE_RECORDING[1 if type_request == self._ACCOUNT_DATA_CHANGING_PREFIX else 2],
            STAGE_BY_PAYLOAD[type_requested_operation]
        )

        callback_markup = _lightscripts.get_inline_keyboard_by_stage(
            recordstage=stage_recording,
            recordtype=type_recording,
            user_lang_code=user_lang_code
        )
        question_text = QUESTION_STATEMENT_BY_CALLBACK_PAYLOAD if type_recording == TYPE_RECORDING[1] else \
            QUESTION_STATEMENT_BY_CALLBACK_PAYLOAD_FINDING

        await self._large_message_renderer.render_main_message(
            user_id=user_id,
            description=question_text[type_requested_operation][user_lang_code],
            markup=callback_markup
        )
        if type_requested_operation in STAGE_BY_PAYLOAD:
            self._database_operation_assistant.start_recording(
                user_id=user_id,
                record_type=type_recording,
                record_stage=stage_recording
            )

    async def handle_finding_cals(self, callback_query: aiogram.types.CallbackQuery, callback_data: dict):
        user_id = callback_query.from_user.id
        user_lang_code = self._database_operation_assistant.get_user_lang_or_default(user_id=user_id)

        try:
            type_requested_operation = callback_data['called_operation']
            finding_mode = None
        except KeyError:
            finding_mode = callback_data['finding_type']
            type_requested_operation = None

        if finding_mode:
            finded_user_id = int()

            if finding_mode == 'spec':
                searching_settings = self._database_operation_assistant.get_user_wishes(user_id=user_id)
                finded_user_id = self._database_operation_assistant.get_user_id_by_params(
                    user_id=user_id,
                    age_range=searching_settings[0],
                    city=searching_settings[1],
                    sex=searching_settings[2]
                )

            elif finding_mode == 'fast':
                finded_user_id = self._database_operation_assistant.get_user_id_without_params(user_id=user_id)

            if not finded_user_id:
                await self._large_message_renderer.render_buffering_message(user_id=user_id,
                                                                            user_lang_code=user_lang_code)
                return

            self._database_operation_assistant.del_user_from_buffer(user_id=finded_user_id)
            finded_user_lang_code = self._database_operation_assistant.get_user_lang_or_default(user_id=user_id)

            for telegram_id in (user_id, finded_user_id):
                await self._large_message_renderer.render_main_message(
                    user_id=telegram_id,
                    description=STATEMENTS_BY_LANG[
                        finded_user_lang_code if telegram_id == finded_user_id else user_lang_code
                    ].find_successful
                )

                self._database_operation_assistant.start_chatting(
                    user_id=telegram_id,
                    interlocator_id=user_id if telegram_id == finded_user_id else finded_user_id
                )

        elif type_requested_operation == 'clarify':
            await self._large_message_renderer.render_clarify_message(user_id=user_id, user_lang_code=user_lang_code)

        elif type_requested_operation == 'back':
            await self._large_message_renderer.render_finding_message(user_id=user_id, user_lang_code=user_lang_code)

    async def handle_sex_call(self, callback_query: aiogram.types.CallbackQuery, callback_data: dict):
        type_requested_operation = callback_data['called_operation']
        user_id = callback_query.from_user.id
        user_lang_code = self._database_operation_assistant.get_user_lang_or_default(user_id=user_id)
        _, type_recording, stage_recording = self._database_operation_assistant.get_recording_condition(user_id=user_id)

        self._registration_data_handler.record_user_param(
            user_id=user_id,
            message_payload=type_requested_operation,
            record_stage=stage_recording,
            record_type=type_recording
        )
        self._database_operation_assistant.increase_recording_stage(user_id=user_id)

        if type_recording == TYPE_RECORDING[0]:
            await self._large_message_renderer.render_main_message(
                user_id=user_id,
                description=STATEMENTS_BY_LANG[user_lang_code].q_desc
            )

        elif type_recording == TYPE_RECORDING[2]:
            await self._large_message_renderer.render_clarify_message(user_id=user_id, user_lang_code=user_lang_code)

    async def handle_buffering_call(self, callback_query: aiogram.types.CallbackQuery, callback_data: dict):
        type_requested_operation = callback_data['called_operation']
        user_id = callback_query.from_user.id
        user_lang_code = self._database_operation_assistant.get_user_lang_or_default(user_id=user_id)

        if type_requested_operation == 'back':
            await self._large_message_renderer.render_profile(user_id=user_id, user_lang_code=user_lang_code)
            self._database_operation_assistant.del_user_from_buffer(user_id=user_id)
            return

        if type_requested_operation == 'fast':
            self._database_operation_assistant.buffering_user_without_params(user_id=user_id)

        elif type_requested_operation == 'specific':
            self._database_operation_assistant.buffering_user_with_params(user_id=user_id)

        await self._large_message_renderer.render_main_message(
            user_id=user_id,
            description=STATEMENTS_BY_LANG[user_lang_code].bufferized_success,
            markup=INLINE_EXIT_BUFFER_KB[user_lang_code]
        )
