import aiogram
import inspect
from typing import Callable, Union

from src.prettybot.bot import _lightscripts
from src.prettybot.bot.dbassistant import database_assistant
from src.prettybot.bot.messages.botmessages import botmessages
from src.prettybot.bot.messages.handlers.eventhandlers import event_handler
from src.prettybot.bot.dbassistant.registrations import registration_data_handler
from src.prettybot.exceptions import exceptions_inspector

from src.prettybot.bot.callback.callback_keyboards import *
from src.config.recording_stages import *


class CallbackHandler:
    _database_operation_assistant: database_assistant.Database
    _bot: aiogram.Bot
    _handling_callback_error_message_to_user = 'error on server'

    def __init__(self, bot_handlers_fields: event_handler.EventHandlersFields):
        self.__dict__ = {param: bot_handlers_fields.__dict__[param]
                         for param in bot_handlers_fields.__dict__
                         if param in CallbackHandler.__annotations__}
        self._callback_request_handler = RequestTypeHandler(bot_handlers_fields=bot_handlers_fields)

    async def handle_callback(self, callback_query: aiogram.types.CallbackQuery) -> None:
        try:
            await self._respond_successful_callback_handling(query_id=callback_query.id)
            await self._handle_callback(callback_query=callback_query)
        except:
            await self._respond_wrong_callback_handling(query_id=callback_query.id,
                                                        alert_text=self._handling_callback_error_message_to_user)

    async def _handle_callback(self, callback_query: aiogram.types.CallbackQuery) -> None:
        user_id, query_id, from_message_id = (callback_query.from_user.id,
                                              callback_query.id,
                                              callback_query.message.message_id)

        user_lang_code = self._database_operation_assistant.get_user_lang_or_default(user_id=user_id)
        _, type_logging, stage_logging = self._database_operation_assistant.get_recording_condition(user_id=user_id)

        payload = _unpack_callback_playload(payload_string=callback_query.data)
        type_request, type_requested_operation = payload.values()

        callback_handler_kwargs = dict(
            type_request=type_request,
            type_requested_operation=type_requested_operation,
            user_id=user_id,
            from_message_id=from_message_id,
            user_lang_code=user_lang_code,
            type_logging=type_logging,
            stage_logging=stage_logging
        )

        callback_handler = self._callback_request_handler.get_handler_by_type_request(type_request=type_request)
        await self._callback_request_handler.handle_request_callback(
            callback_handler=callback_handler, **callback_handler_kwargs
        )

    async def _respond_wrong_callback_handling(self, query_id: int, alert_text: str) -> None:
        await self._bot.answer_callback_query(query_id, text=alert_text, show_alert=True)

    async def _respond_successful_callback_handling(self, query_id: int) -> None:
        await self._bot.answer_callback_query(query_id, show_alert=False)


class RequestTypeHandler:
    on_keyerror_return = KeyError
    on_exception_return = BaseException
    _database_operation_assistant: database_assistant.Database
    _bot: aiogram.Bot
    _large_message_renderer: botmessages.MainMessagesRenderer
    _registration_data_handler: registration_data_handler.RegistrationParamsHandler

    def __init__(self, bot_handlers_fields: event_handler.EventHandlersFields):
        self.__dict__ = {param: bot_handlers_fields.__dict__[param]
                         for param in bot_handlers_fields.__dict__
                         if param in RequestTypeHandler.__annotations__}

    def get_handler_by_type_request(self, type_request: str) -> Callable[[dict], None]:
        return self._handler_by_type_request[type_request]

    async def handle_request_callback(
            self, callback_handler: Callable[[dict], None],
            **handler_kwargs: dict) -> Union[KeyError, None]:
        try:
            await callback_handler(self, **handler_kwargs)
        except KeyError as exception:
            return self.on_keyerror_return(
                exceptions_inspector.get_traceback(exception=exception, stack=inspect.stack())
            )
        except Exception as exception:
            return self.on_exception_return(
                exceptions_inspector.get_traceback(exception=exception, stack=inspect.stack())
            )

    async def _handle_main_type_request(self, **handler_kwargs) -> None:
        type_requested_operation = handler_kwargs['type_requested_operation']
        user_id = handler_kwargs['user_id']
        from_message_id = handler_kwargs['from_message_id']
        user_lang_code = handler_kwargs['user_lang_code']

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

    async def _handle_changing_type_request(self, **handler_kwargs) -> None:
        type_request = handler_kwargs['type_request']
        type_requested_operation = handler_kwargs['type_requested_operation']
        user_id = handler_kwargs['user_id']
        from_message_id = handler_kwargs['from_message_id']
        user_lang_code = handler_kwargs['user_lang_code']

        if type_requested_operation != 'back':
            callback_markup = _lightscripts.get_inline_keyboard_by_stage(
                recordstage=STAGE_BY_PAYLOAD[type_requested_operation],
                recordtype=TYPE_RECORDING[1 if type_request == 'change' else 2],
                user_lang_code=user_lang_code
            )

            await self._large_message_renderer.render_main_message(
                user_id=user_id,
                description=(QUESTION_STATEMENT_BY_CALLBACK_PAYLOAD
                             if type_request == 'change' else
                             QUESTION_STATEMENT_BY_CALLBACK_PAYLOAD_FINDING
                             )[type_requested_operation][user_lang_code],
                markup=callback_markup
            )

        elif type_requested_operation == 'back':
            await self._bot.edit_message_reply_markup(chat_id=user_id,
                                                      message_id=from_message_id,
                                                      reply_markup=INLINE_PROFILE_KB[user_lang_code])

        if type_requested_operation in STAGE_BY_PAYLOAD.keys():
            self._database_operation_assistant.start_recording(
                user_id=user_id,
                record_type=TYPE_RECORDING[1 if type_request == 'change' else 2],
                record_stage=STAGE_BY_PAYLOAD[type_requested_operation]
            )

    async def _handle_sex_type_request(self, **handler_kwargs) -> None:
        type_requested_operation = handler_kwargs['type_requested_operation']
        user_id = handler_kwargs['user_id']
        user_lang_code = handler_kwargs['user_lang_code']
        stage_logging = handler_kwargs['stage_logging']
        type_logging = handler_kwargs['type_logging']

        self._registration_data_handler.record_user_param(
            user_id=user_id,
            message_payload=type_requested_operation,
            record_stage=stage_logging,
            record_type=type_logging
        )

        if type_logging == TYPE_RECORDING[0]:
            await self._large_message_renderer.render_main_message(
                user_id=user_id,
                description=STATEMENTS_BY_LANG[user_lang_code].q_desc
            )

        elif type_logging == TYPE_RECORDING[2]:
            await self._large_message_renderer.render_finding_message(user_id=user_id, user_lang_code=user_lang_code)

        self._database_operation_assistant.increase_recording_stage(user_id=user_id)

    async def _handle_find_type_request(self, **handler_kwargs) -> None:
        type_requested_operation = handler_kwargs['type_requested_operation']
        user_id = handler_kwargs['user_id']
        user_lang_code = handler_kwargs['user_lang_code']

        if type_requested_operation.split('&')[0] == 'start':
            searching_mode, finded_user_id = type_requested_operation.split('&')[1], int()

            if searching_mode == 'spec':
                searching_settings = self._database_operation_assistant.get_user_wishes(user_id=user_id)
                finded_user_id = self._database_operation_assistant.get_user_id_by_params(user_id=user_id,
                                                                                          age_range=searching_settings[
                                                                                              0],
                                                                                          city=searching_settings[1],
                                                                                          sex=searching_settings[2])

            elif searching_mode == 'fast':
                finded_user_id = self._database_operation_assistant.get_user_id_without_params(user_id=user_id)

            if not finded_user_id:
                await self._large_message_renderer.render_buffering_message(user_id=user_id,
                                                                            user_lang_code=user_lang_code)
                return

            finded_user_lang_code = self._database_operation_assistant.get_user_lang_or_default(user_id=user_id)

            for telegram_id in (user_id, finded_user_id):
                await self._large_message_renderer.render_main_message(
                    user_id=telegram_id,
                    description=STATEMENTS_BY_LANG[
                        finded_user_lang_code if telegram_id == finded_user_id else user_lang_code
                    ].find_successful)

                self._database_operation_assistant.start_chatting(user_id=telegram_id,
                                                                  interlocator_id=user_id
                                                                  if telegram_id == finded_user_id
                                                                  else finded_user_id
                                                                  )

            self._database_operation_assistant.del_user_from_buffer(user_id=finded_user_id)

        elif type_requested_operation == 'clarify':
            await self._large_message_renderer.render_clarify_message(
                user_id=user_id,
                user_lang_code=user_lang_code)

        elif type_requested_operation == 'back':
            await self._large_message_renderer.render_finding_message(
                user_id=user_id,
                user_lang_code=user_lang_code)

    async def _handle_buffering_type_request(self, **handler_kwargs):
        type_requested_operation = handler_kwargs['type_requested_operation']
        user_id = handler_kwargs['user_id']
        user_lang_code = handler_kwargs['user_lang_code']

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

    _handler_by_type_request = {
        'main': _handle_main_type_request,
        'change': _handle_changing_type_request,
        'changewish': _handle_changing_type_request,
        'sex': _handle_sex_type_request,
        'find': _handle_find_type_request,
        'buffer': _handle_buffering_type_request,
    }


def _unpack_callback_playload(payload_string: str) -> dict:
    return dict(type_request=payload_string.split('%')[0], type_requested_operation=payload_string.split('%')[1])
