import aiogram
from src.bot.db.database_assistant import DatabaseScripts


def prehandler(handler_func):
    async def wrapper(*args):
        message: aiogram.types.Message = args[0]
        user_id = message.from_user.id
        # bufferized = self._database_assistant.get_user_data_by_table(
        #         user_id=user_id,
        #         table_name=''
        # )

        if message.chat.type == 'private':
            await handler_func(message, user_id)

    return wrapper
