import aiogram

from src.prettybot.bot.messages.handlers.eventhandlers.event_handler import EventHandlersFields
from src.prettybot.bot.dbassistant.database_assistant import Database
from src.prettybot.bot.messages.botmessages.botmessages import MainMessagesRenderer
from src.prettybot.exceptions import exceptions
from src.config.recording_stages import *


class CommandsHandler:
    _database_operation_assistant: Database
    _large_message_renderer: MainMessagesRenderer

    def __init__(self, bot_handlers_fields: EventHandlersFields):
        self.__dict__ = {param: bot_handlers_fields.__dict__[param]
                         for param in bot_handlers_fields.__dict__
                         if param in CommandsHandler.__annotations__}

    async def handle_start(self, message: aiogram.types.Message, user_id: int, user_lang_code: str):
        try:
            user_recording_condition = self._database_operation_assistant.get_recording_condition(user_id=user_id)
        except exceptions.UserDataNotFoundException:
            user_recording_condition = None

        if user_recording_condition:

            recording, record_type, record_stage = user_recording_condition

            if recording and record_type == MAIN_RECORDING_TYPE:
                await self._large_message_renderer.render_disappearing_message(
                    user_id=user_id,
                    description=STATEMENTS_BY_LANG[user_lang_code].help,
                    delay_before_deleting=LONG_DELAY
                )
            else:
                if recording:
                    self._database_operation_assistant.stop_recording(user_id=user_id)

                await self._large_message_renderer.render_profile(user_id=user_id, user_lang_code=user_lang_code)

        else:
            self._database_operation_assistant.add_new_user(
                user_id=user_id,
                fname=message.from_user.first_name,
                lname=message.from_user.last_name,
                telegname=message.chat.username,
                date_message=message.date
            )

            await self._large_message_renderer.render_main_message(
                user_id=user_id,
                description=BASE_STATEMENTS.welcome.format(message.from_user.first_name)
            )

    async def handle_help(self, user_id: int, user_lang_code: str, **_):
        await self._large_message_renderer.render_disappearing_message(
            user_id=user_id,
            description=STATEMENTS_BY_LANG[user_lang_code].help,
            delay_before_deleting=MEDIUM_DELAY)

    async def handle_restart(self, **handler_kwargs):
        await self._large_message_renderer.delete_main_message_from_all(user_id=handler_kwargs['user_id'])
        self._database_operation_assistant.delete_user_records(user_id=handler_kwargs['user_id'])

    async def handle_change_lang(self, message: aiogram.types.Message, user_id: int, **_):
        lang_code = message.text[1:3]
        self._database_operation_assistant.change_user_lang(user_id=user_id, lang_code=lang_code)
        await self._large_message_renderer.render_disappearing_message(
            user_id=user_id,
            description=STATEMENTS_BY_LANG[lang_code].change_lang_good,
            delay_before_deleting=DEFAULT_DELAY
        )

    async def handle_stop_chatting(self, user_id: int, user_lang_code: str, **_):
        interlocutor_id = self._database_operation_assistant.get_interlocator_id(user_id=user_id)
        interlocutor_lang_code = self._database_operation_assistant.get_user_lang_or_default(user_id=interlocutor_id)

        for telegram_id in (user_id, interlocutor_id):
            self._database_operation_assistant.stop_chatting(user_id=telegram_id)

        await self._large_message_renderer.render_profile(user_id=user_id, user_lang_code=user_lang_code)
        await self._large_message_renderer.render_profile(user_id=interlocutor_id, user_lang_code=interlocutor_lang_code)

        await self._large_message_renderer.render_disappearing_message(
            user_id=user_id,
            description=STATEMENTS_BY_LANG[user_lang_code].end_chatting,
            delay_before_deleting=DEFAULT_DELAY)

        await self._large_message_renderer.render_disappearing_message(
                    user_id=interlocutor_id,
                    description=STATEMENTS_BY_LANG[interlocutor_lang_code].end_chatting,
                    delay_before_deleting=DEFAULT_DELAY)