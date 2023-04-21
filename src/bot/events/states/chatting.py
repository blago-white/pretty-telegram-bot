from aiogram.dispatcher.filters.state import StatesGroup, State
from ._custom_states import ChattingState


class Chatting(StatesGroup):
    ischatting = ChattingState()
