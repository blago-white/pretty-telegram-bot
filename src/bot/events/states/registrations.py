from aiogram.dispatcher.filters.state import StatesGroup, State
from src.bot.config.recording_stages import TYPE_RECORDING


class InitialRegistration(StatesGroup):
    age = State()
    cty = State()
    sex = State()
    dsc = State()
    pht = State()

    def __str__(self):
        return TYPE_RECORDING[0]


class AccountRegistration(StatesGroup):
    age = State()
    cty = State()
    sex = State()
    dsc = State()
    pht = State()

    def __str__(self):
        return TYPE_RECORDING[1]


class WishesRegistration(StatesGroup):
    age = State()
    cty = State()
    sex = State()

    def __str__(self):
        return TYPE_RECORDING[2]
