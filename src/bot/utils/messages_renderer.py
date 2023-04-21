import aiogram.types

from ..utils import lightscripts, chat_interactor
from ..dbassistant import database_assistant
from ..utils import async_delayer

from ..utils.exceptions import exceptions

from ..keyboards.callback_keyboards import *
from ..config.pbconfig import *

__all__ = ['MainMessageTextGenerator',
           'MainMessagesRenderer']


class MainMessageTextGenerator:
    def __init__(self, database_operation_assistant):
        self._database_operation_assistant = database_operation_assistant

    def generate_profile_body(self, user_id: int, user_lang_code: str) -> str:
        """
        :param user_id: telegram id of user
        :param user_lang_code: user language
        :returns: user profile body
        """

        account_data = self._database_operation_assistant.get_user_data_by_table(user_id=user_id,
                                                                                 table_name='users_info')[0]
        username = self._database_operation_assistant.get_user_data_by_table(user_id=user_id, table_name='users')[0][1]
        age_declination = _get_age_declination(age=account_data[1])
        city = account_data[3].capitalize()

        return _fill_profile_template(name=username,
                                      age=account_data[1],
                                      declination=age_declination,
                                      city=city,
                                      description=account_data[7],
                                      lang=user_lang_code)

    def generate_finding_params_message(self, user_id: int, user_lang_code: str) -> str:
        user_data = self._database_operation_assistant.get_user_wishes(user_id=user_id)
        age_interval = user_data[0]
        user_sex = lightscripts.convert_sex_type(user_data[2])

        return _fill_finding_params_template(city=user_data[1],
                                             age_interval=age_interval,
                                             sex=user_sex,
                                             lang=user_lang_code)


class MainMessagesRenderer:
    _database_operation_assistant: database_assistant.BotDatabase
    _message_interactor: chat_interactor.ChatMessagesInteractor
    _main_message_text_generator: MainMessageTextGenerator

    def __init__(
            self, database_operation_assistant: database_assistant.BotDatabase,
            message_interactor: chat_interactor.ChatMessagesInteractor,
            bot: aiogram.Bot):
        self._message_interactor = message_interactor
        self._database_operation_assistant = database_operation_assistant
        self._bot = bot
        self._main_message_text_generator = MainMessageTextGenerator(
            database_operation_assistant=database_operation_assistant
        )

    async def render_profile(
            self, user_id: int,
            user_lang_code: str) -> None:

        profile_photo_id = self._database_operation_assistant.get_photo_id(user_id=user_id)
        if not profile_photo_id:
            raise exceptions.UserDataNotFoundException

        profile_body = self._main_message_text_generator.generate_profile_body(user_id=user_id,
                                                                               user_lang_code=user_lang_code)

        sended_message_id = await self._message_interactor.send_photo(user_id=user_id,
                                                                      photo_id=profile_photo_id,
                                                                      description=profile_body,
                                                                      keyboard=INLINE_PROFILE_KB[user_lang_code]
                                                                      )

        await self._update_main_message(user_id=user_id, sended_message_id=sended_message_id)

    async def render_finding_message(
            self, user_id: int,
            user_lang_code: str) -> None:
        await self.render_main_message(user_id=user_id,
                                       description=STATEMENTS_BY_LANG[user_lang_code].clarify,
                                       markup=INLINE_MODE_FINDING_KB[user_lang_code])

    async def render_buffering_message(
            self, user_id: int,
            user_lang_code: str
    ):
        await self.render_main_message(user_id=user_id,
                                       description=STATEMENTS_BY_LANG[user_lang_code].buffering_question,
                                       markup=INLINE_BUFFERING_QUESTION_KB[user_lang_code])

    async def render_clarify_message(
            self, user_id,
            user_lang_code: str) -> None:
        message_body = self._main_message_text_generator.generate_finding_params_message(
            user_id=int(user_id),
            user_lang_code=str(user_lang_code)
        )

        await self.render_main_message(user_id=int(user_id),
                                       description=str(message_body),
                                       markup=INLINE_CHANGE_PARAMS_FIND_KB[user_lang_code])

    async def render_disappearing_message(
            self, user_id: int,
            description: str,
            delay_before_deleting: int) -> None:
        sended_message_id = await self._message_interactor.send(user_id=int(user_id), description=str(description))
        await async_delayer.postpone_async_task(
            self._message_interactor.delete_message(user_id=user_id, message_id=sended_message_id),
            delay=delay_before_deleting
        )

    async def render_main_message(
            self, user_id: int,
            description: str,
            markup: aiogram.types.InlineKeyboardMarkup = INLINE_EMPTY_KB) -> None:
        sended_message_id = await self._message_interactor.send(user_id=user_id, description=description, markup=markup)
        await self._update_main_message(user_id=user_id, sended_message_id=sended_message_id)

    async def delete_main_message_from_all(self, user_id: int) -> None:
        message_id = self._database_operation_assistant.get_main_message(user_id=int(user_id))
        if message_id:
            await self._message_interactor.delete_message(user_id=user_id, message_id=message_id)
            self._database_operation_assistant.delete_main_message(user_id=user_id)

    async def _update_main_message(self, user_id: int, sended_message_id: int) -> None:
        try:
            await self._delete_main_message_from_chat(user_id=user_id)
            self._database_operation_assistant.set_main_message_id(user_id=user_id, message_id=sended_message_id)
        except TypeError:
            raise exceptions.UserDataNotFoundException

    async def _delete_main_message_from_chat(self, user_id: int) -> None:
        message_id = self._database_operation_assistant.get_main_message(user_id=int(user_id))
        if message_id:
            await self._message_interactor.delete_message(user_id=user_id, message_id=message_id)


def _fill_profile_template(**values: dict) -> str:
    try:
        profile_template = STATEMENTS_BY_LANG[values['lang']].profile_templ
        profile_template = profile_template.format(
            name=values['name'],
            age=values['age'],
            declination=values['declination'],
            city=values['city'],
            desc=values['description']
        )

        return profile_template

    except KeyError:
        return KeyError('not full arguments')


def _fill_finding_params_template(**values: dict) -> str:
    try:
        finding_params_template = STATEMENTS_BY_LANG[values['lang']].change_find_params
        finding_params_template = finding_params_template.format(
            values['city'],
            int(values['age_interval'].lower),
            int(values['age_interval'].upper),
            values['sex']
        )

        return finding_params_template

    except KeyError:
        return KeyError('not full arguments')


def _get_age_declination(age: int) -> str:
    declination_id = 1 if age % 10 == 1 else (2 if 1 < age % 10 < 5 else 0)
    return AGE_DECLINATIONS[declination_id]
