import aiogram

from ...botmessages import botmessages
from ... import chat_interactor
from ...handlers.user_answers_handler import user_answers_handler

from src.prettybot.bot import _lightscripts
from src.prettybot.bot.dbassistant import database_assistant
from src.prettybot.bot.dbassistant.registrations.registration_data_handler import RegistrationParamsHandler

from src.config.recording_stages import *


class ContentTypesHandler:
    def __init__(
            self, database_operation_assistant: database_assistant.BotDatabase,
            message_interactor: chat_interactor.ChatMessagesInteractor,
            large_message_renderer: botmessages.MainMessagesRenderer,
            registration_data_handler: RegistrationParamsHandler
    ):
        self._database_operation_assistant = database_operation_assistant
        self._message_interactor = message_interactor
        self._large_message_renderer = large_message_renderer
        self._registration_data_handler = registration_data_handler

    async def handle_photo(self, message: aiogram.types.Message, user_id: int, user_lang_code: str) -> None:
        recording, record_type, record_stage = self._database_operation_assistant.get_recording_condition(
            user_id=user_id
        )

        file_id = message.photo[0]['file_id']
        if recording and record_stage == STAGES_RECORDING[4]:
            self._registration_data_handler.record_user_param(
                user_id=user_id,
                message_payload=file_id,
                record_stage=record_stage,
                record_type=record_type)

            await self._large_message_renderer.render_profile(user_id=user_id, user_lang_code=user_lang_code)
            self._database_operation_assistant.stop_recording(user_id=user_id)

    async def handle_text(self, message: aiogram.types.Message, user_id: int, user_lang_code: str) -> None:
        if self._database_operation_assistant.user_in_chatting(user_id=user_id):
            interlocator_id = self._database_operation_assistant.get_interlocator_id(user_id=user_id)
            await self._message_interactor.send(user_id=interlocator_id, description=message.text)
            return

        user_recording_data = self._database_operation_assistant.get_recording_condition(user_id=user_id)

        if not user_recording_data or not user_recording_data[0]:
            return

        recording, record_type, record_stage = user_recording_data
        statement_for_stage = user_answers_handler.handle_message(
            message_text=message.text,
            user_lang_code=user_lang_code,
            record_type=record_type,
            record_stage=record_stage)
        inline_markup_for_stage = _lightscripts.get_inline_keyboard_by_stage(
            recordstage=_lightscripts.get_shifted_recordstage_for_main_record_type(
                record_type=record_type,
                record_stage=record_stage,
                user_answer_is_valid=statement_for_stage[0]),
            recordtype=record_type,
            user_lang_code=user_lang_code,
        )
        if statement_for_stage[0]:
            self._registration_data_handler.record_user_param(
                user_id=user_id,
                message_payload=message.text,
                record_stage=record_stage,
                record_type=record_type)

            handling_function = self._HANDLING_FUNCTIONS_BY_RECORDTYPE[record_type]

            if record_type == TYPE_RECORDING[0]:
                args = user_id, statement_for_stage[-1], inline_markup_for_stage

            else:
                args = user_id, user_lang_code

            await handling_function(self, *args)

        elif not statement_for_stage[0] and statement_for_stage[1]:
            await self._large_message_renderer.render_main_message(
                user_id=user_id,
                description=statement_for_stage[1],
                markup=inline_markup_for_stage)

    async def _final_handle_registration_message(
            self, user_id: int,
            description: str,
            markup: aiogram.types.InlineKeyboardMarkup) -> None:
        await self._large_message_renderer.render_main_message(user_id=user_id, description=description, markup=markup)
        self._database_operation_assistant.increase_recording_stage(user_id=user_id)

    async def _final_handle_changing_account_info_message(self, user_id: int, user_lang_code: str) -> None:
        await self._large_message_renderer.render_profile(user_id=user_id, user_lang_code=user_lang_code)
        self._database_operation_assistant.stop_recording(user_id=user_id)

    async def _final_handle_changing_searching_params_message(self, user_id: int, user_lang_code: str) -> None:
        await self._large_message_renderer.render_finding_message(user_id=user_id, user_lang_code=user_lang_code)
        self._database_operation_assistant.stop_recording(user_id=user_id)

    _HANDLING_FUNCTIONS_BY_RECORDTYPE = {
        TYPE_RECORDING[0]: _final_handle_registration_message,
        TYPE_RECORDING[1]: _final_handle_changing_account_info_message,
        TYPE_RECORDING[2]: _final_handle_changing_searching_params_message}
