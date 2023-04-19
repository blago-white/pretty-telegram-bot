from typing import Callable, Union
import aiogram

from src.prettybot import bot
from src.prettybot.bot.events import chat_interactor
from src.prettybot.bot.dbassistant import database_assistant
from src.prettybot.exceptions import exceptions
from src.config.pbconfig import *


class _UserStateValidators:
    def __init__(self, database_assistant_: database_assistant.BotDatabase):
        self._database_operation_assistant = database_assistant_

    def validate_user_state(self, message: aiogram.types.Message, user_chatting_condition: Union[bool, None]) -> bool:
        chat_type_valid = self._validate_chat_type(message_chat_type=message.chat.type)
        chatting_condition_valid = _validate_chatting_condition(is_command=bool(message.entities),
                                                                message_text=message.text,
                                                                user_chatting_condition=user_chatting_condition)

        return chat_type_valid and chatting_condition_valid

    def get_chatting_status_or_none(self, user_id: int, message_text: str) -> Union[bool, None]:
        try:
            return self._database_operation_assistant.user_in_chatting(user_id=user_id)
        except Exception as exception:
            if (exception.__class__ is exceptions.UserDataNotFoundException) \
                    and (message_text[1:] in BOT_COMMANDS['start']):
                return None

    @staticmethod
    def _validate_chat_type(message_chat_type: str) -> bool:
        return message_chat_type in ALLOWED_CHAT_TYPES


class MessagePreHandler:
    _database_operation_assistant: database_assistant.BotDatabase
    _message_interactor: chat_interactor.ChatMessagesInteractor

    def __init__(self, database_assistant_, message_interactor):
        self._message_interactor = message_interactor
        self._database_operation_assistant = database_assistant_
        self._state_validator = _UserStateValidators(database_assistant_=database_assistant_)

    async def prehandle(self, handler_func: Callable[[dict], None], message: aiogram.types.Message):
        """
        :param message:
        :param handler_func: async handler function
        :return:
        """

        user_id = message.from_user.id
        user_lang_code = self._database_operation_assistant.get_user_lang_or_default(user_id=message.from_user.id)
        user_chatting_condition = self._state_validator.get_chatting_status_or_none(user_id=user_id,
                                                                                    message_text=message.text)
        user_state_valid_to_handling = self._state_validator.validate_user_state(
            message=message,
            user_chatting_condition=user_chatting_condition
        )

        if user_state_valid_to_handling:
            await self._try_handle_message(handler_function=handler_func, message=message,
                                           user_lang_code=user_lang_code)

        if not user_chatting_condition:
            await self._message_interactor.delete_message(user_id=user_id, message_id=message.message_id)

    async def _try_handle_message(self, handler_function, message: aiogram.types.Message, user_lang_code: str):
        try:
            await handler_function(message=message, user_id=message.from_user.id, user_lang_code=user_lang_code)
        except Exception as exception:
            await self._message_interactor.send_except_message(user_id=message.from_user.id,
                                                               user_lang_code=user_lang_code)
            print('handling error: ', exception)


def _validate_chatting_condition(
        is_command: bool, message_text: str, user_chatting_condition: Union[bool, None]) -> bool:
    if user_chatting_condition is None:
        if message_text[1:] in BOT_COMMANDS['start']:
            return True
        return

    if (user_chatting_condition and is_command and message_text[1:] not in BOT_COMMANDS['end']) \
            or (not user_chatting_condition and is_command and message_text[1:] in BOT_COMMANDS['end']):
        return

    return True
