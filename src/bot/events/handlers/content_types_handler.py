import aiogram

from ...events.states import registrations
from ...utils.user_answers_handler import user_answers_handler

from ...utils import lightscripts, chat_interactor, messages_renderer
from ...dbassistant import database_assistant
from ...dbassistant.registrations.registration_data_handler import RegistrationParamsHandler

from ...config.recording_stages import *


class ContentTypesHandler:
    def __init__(
            self, database_operation_assistant: database_assistant.BotDatabase,
            message_interactor: chat_interactor.ChatMessagesInteractor,
            large_message_renderer: messages_renderer.MainMessagesRenderer,
            registration_data_handler: RegistrationParamsHandler
    ):
        self._database_operation_assistant = database_operation_assistant
        self._message_interactor = message_interactor
        self._large_message_renderer = large_message_renderer
        self._registration_data_handler = registration_data_handler

    async def handle_photo(
            self, message: aiogram.types.Message,
            state: aiogram.dispatcher.FSMContext) -> None:
        user_id = message.from_user.id
        file_id = message.photo[0]['file_id']
        user_lang_code = self._database_operation_assistant.get_user_lang_or_default(user_id=user_id)

        current_state = await state.get_state()
        record_type, record_stage = (TYPE_RECORDING_BY_STATE_GROUP[current_state.split(':')[0]],
                                     current_state.split(':')[-1])

        self._registration_data_handler.record_user_param(
                user_id=user_id,
                message_payload=file_id,
                record_stage=record_stage,
                record_type=record_type)

        await self._large_message_renderer.render_profile(user_id=user_id, user_lang_code=user_lang_code)
        await state.finish()

    async def handle_useless_message(
            self, message: aiogram.types.Message,
            state: aiogram.dispatcher.FSMContext):
        await self._message_interactor.delete_message(user_id=message.from_user.id, message_id=message.message_id)

    async def handle_conversation_text(
            self, message: aiogram.types.Message,
            state: aiogram.dispatcher.FSMContext):
        interlocutor_id = await state.get_data()
        print(message.from_user.id, ' -- ', interlocutor_id)
        await self._message_interactor.send(user_id=interlocutor_id['interlocutor_id'], description=message.text)

    async def handle_text(
            self, message: aiogram.types.Message,
            state: aiogram.dispatcher.FSMContext) -> None:
        user_id = message.from_user.id
        user_lang_code = self._database_operation_assistant.get_user_lang_or_default(user_id=user_id)

        current_state = await state.get_state()
        recording, record_type, record_stage = (True,
                                                TYPE_RECORDING_BY_STATE_GROUP[current_state.split(':')[0]],
                                                current_state.split(':')[-1])

        statement_for_stage = user_answers_handler.handle_message(
            message_text=message.text,
            user_lang_code=user_lang_code,
            record_type=record_type,
            record_stage=record_stage)
        inline_markup_for_stage = lightscripts.get_inline_keyboard_by_stage(
            recordstage=lightscripts.get_shifted_recordstage_for_main_record_type(
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
                args = user_id, state, statement_for_stage[-1], inline_markup_for_stage

            else:
                args = user_id, state, user_lang_code

            await handling_function(self, *args)

        elif not statement_for_stage[0] and statement_for_stage[1]:
            await self._large_message_renderer.render_main_message(
                user_id=user_id,
                description=statement_for_stage[1],
                markup=inline_markup_for_stage)

    async def _final_handle_registration_message(
            self, user_id: int,
            state: aiogram.dispatcher.FSMContext,
            description: str,
            markup: aiogram.types.InlineKeyboardMarkup) -> None:
        await self._large_message_renderer.render_main_message(user_id=user_id, description=description, markup=markup)
        await state.set_state(await registrations.InitialRegistration.next())

    async def _final_handle_changing_account_info_message(
            self, user_id: int,
            state: aiogram.dispatcher.FSMContext,
            user_lang_code: str) -> None:
        await self._large_message_renderer.render_profile(user_id=user_id, user_lang_code=user_lang_code)
        await state.finish()

    async def _final_handle_changing_searching_params_message(
            self, user_id: int,
            state: aiogram.dispatcher.FSMContext,
            user_lang_code: str) -> None:
        await self._large_message_renderer.render_finding_message(user_id=user_id, user_lang_code=user_lang_code)
        await state.finish()

    _HANDLING_FUNCTIONS_BY_RECORDTYPE = {
        TYPE_RECORDING[0]: _final_handle_registration_message,
        TYPE_RECORDING[1]: _final_handle_changing_account_info_message,
        TYPE_RECORDING[2]: _final_handle_changing_searching_params_message}
