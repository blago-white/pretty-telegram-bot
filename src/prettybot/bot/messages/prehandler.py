import types
import aiogram

from src.prettybot import bot


class PreHandler:

    _database_assistant: str

    def __init__(self, database_assistant):
        self._database_assistant = database_assistant

    def prehandle(
            self,
            handler_func: types.FunctionType,
            message: aiogram.types.Message):

        """
        :param message:
        :param handler_func: async handler function
        :return:
        """

        async def wrapper():
            user_id = message.from_user.id

            bufferized = self._database_assistant.get_user_data_by_table(
                    user_id=user_id,
                    table_name='users_searching_buffer'
            )
            print(bufferized)

            if message.chat.type == 'private':
                await handler_func(message, user_id)

        return wrapper()
