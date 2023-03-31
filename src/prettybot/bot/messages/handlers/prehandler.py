import types
import aiogram

from src.prettybot import bot
from src.prettybot.bot.messages import chat_interaction
from src.prettybot.bot.dbassistant import database_assistant
from src.config import pbconfig


class MessagePreHandler:
    database_operation_assistant: database_assistant.Database
    _message_sender: chat_interaction.MessageSender
    _message_deleter: chat_interaction.MessageDeleter

    def __init__(self, database_assistant_, message_sender, message_deleter):
        self._message_sender = message_sender
        self._message_deleter = message_deleter
        self.database_operation_assistant = database_assistant_

    def prehandle(
            self,
            handler_func,
            message: aiogram.types.Message):

        """
        :param message:
        :param handler_func: async handler function
        :return:
        """

        async def wrapper():
            if message.chat.type == 'private':

                user_id = message.from_user.id
                on_chatting = self.database_operation_assistant.get_chatting_condition(
                    user_id=user_id)

                if on_chatting and message.entities and message.text[1:] != pbconfig.BOT_COMMANDS['end'][0]:
                    await self._message_deleter.delete_message(user_id=user_id, message_id=message.message_id)
                    return

                user_lang_code = self.database_operation_assistant.get_user_lang_or_default(user_id=user_id)

                await self.try_handle_message(handler_function=handler_func,
                                              message=message,
                                              user_lang_code=user_lang_code)

                await self._message_deleter.delete_message(user_id=user_id, message_id=message.message_id)

        return wrapper()

    async def try_handle_message(self, handler_function, message: aiogram.types.Message, user_lang_code: str):
        try:
            await handler_function(message=message, user_id=message.from_user.id, user_lang_code=user_lang_code)
        except Exception as exception:
            await self._message_sender.send_except_message(user_id=message.from_user.id, user_lang_code=user_lang_code)
            raise exception
