import aiogram

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from src.bot.utils.chat_interactor import ChatMessagesInteractor
from ..states.chatting import Chatting


class TextMiddleware(BaseMiddleware):
    def __init__(self, chat_interactor: ChatMessagesInteractor, dispatcher: aiogram.Dispatcher):
        self._chat_interactor = chat_interactor
        self._dispatcher = dispatcher
        super(TextMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        user_state = self._dispatcher.current_state(user=message.from_user.id, chat=message.chat.id)
        user_state = await user_state.get_state()
        if user_state != str(Chatting.ischatting) or message.text == '/end':
            await self._chat_interactor.delete_message(user_id=message.from_user.id, message_id=message.message_id)
