import aiogram.types
from aiogram.dispatcher.filters.builtin import StateFilter


class UserNotChattingFilter(StateFilter):
    async def check(self, message: aiogram.types.Message) -> bool:
        chat, user = self.get_target(message)
        state = await self.dispatcher.storage.get_state(chat=chat, user=user)
        return state not in str(self.states) if state is not None else True
