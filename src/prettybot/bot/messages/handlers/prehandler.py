import time
from typing import Union
import types
import aiogram

from src.prettybot import bot
from src.prettybot.bot.messages import tgmessages
from src.prettybot.bot.db import database_assistant
from src.prettybot.bot.messages.handlers import msghandlers


class PreHandler:
    database_operation_assistant: database_assistant.Database
    _message_sender: tgmessages.MessageSender
    _message_deleter: tgmessages.MessageDeleter

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
            user_id = message.from_user.id

            bufferized = self.database_operation_assistant.get_user_data_by_table(
                user_id=user_id,
                table_name='users_searching_buffer'
            ).object

            if message.chat.type == 'private':
                try:
                    await handler_func(message,
                                       user_id,
                                       self.database_operation_assistant.get_user_lang_code(user_id=user_id)
                                       )

                except Exception as e:
                    print(e)
                    await self._message_sender.send_except_message(
                        user_id=user_id,
                        user_lang_code=self.database_operation_assistant.get_user_lang_code(user_id=user_id))

                await self._message_deleter.delete_message(user_id=user_id, idmes=message.message_id)

        return wrapper()
