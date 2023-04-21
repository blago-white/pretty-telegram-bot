from aiogram.dispatcher.filters.state import State
from aiogram.dispatcher.dispatcher import Dispatcher


class ChattingState(State):
    def __str__(self):
        return self.state

    async def set(self, user_id: int = None):
        state = Dispatcher.get_current().current_state(user=user_id)
        await state.set_state(self.state)

    async def finish(self, user_id: int = None):
        state = Dispatcher.get_current().current_state(user=user_id)
        await state.finish()
