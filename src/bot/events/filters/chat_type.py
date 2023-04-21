from typing import Container

from aiogram.dispatcher.filters.builtin import ChatTypeFilter, ChatType
from aiogram.types import Message

from src.bot.config.pbconfig import ALLOWED_CHAT_TYPES


class UserChatTypeFilter(ChatTypeFilter):
    def __init__(self, chat_type: Container[ChatType]):
        super().__init__(chat_type)

    async def check(self, message: Message) -> bool:
        return message.chat.type in ALLOWED_CHAT_TYPES
