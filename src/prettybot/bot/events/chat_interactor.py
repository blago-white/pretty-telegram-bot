import aiogram.types
from typing import Union

from src.prettybot.bot.callback.callback_keyboards import *
from src.config.pbconfig import *

__all__ = ['ChatMessagesInteractor']


class ChatMessagesInteractor:
    bot: aiogram.Bot

    def __init__(self, bot: aiogram.Bot) -> None:
        self.bot = bot

    async def send_photo(
            self,
            user_id: int,
            photo_id: str,
            description: str = None,
            parse_mode: str = 'HTML',
            keyboard: aiogram.types.InlineKeyboardMarkup = INLINE_EMPTY_KB) -> int:

        """
        :param user_id: integer, user id
        :param photo_id: string, bot id of file photo
        :param description: string, description to photo
        :param parse_mode: bot parsemode, default = HTML
        :param keyboard: reply inline keyboard, sending with photo

        :returns: sended message id
        :raise Exception: if operation failed
        """
        try:
            sending_response = await self.bot.send_photo(chat_id=user_id,
                                                         photo=photo_id,
                                                         caption=description,
                                                         reply_markup=keyboard,
                                                         parse_mode=parse_mode)

            return sending_response.message_id

        except Exception as exception:
            raise exception

    async def send(
            self,
            user_id: int,
            description: str = None,
            parse_mode: str = 'HTML',
            markup: aiogram.types.InlineKeyboardMarkup = None
    ) -> int:

        """
        :param user_id: integer, user id
        :param description: string, sending with photo_id
        :param parse_mode: bot parsemode, default = HTML
        :param markup: bot markup, sended with message

        :returns: sended message id
        """

        try:
            sending_response = await self.bot.send_message(chat_id=user_id,
                                                           text=description,
                                                           parse_mode=parse_mode,
                                                           reply_markup=markup)

        except Exception as exception:
            raise exception

        return sending_response.message_id

    async def send_except_message(
            self,
            user_id: int,
            description: str = None,
            user_lang_code: str = DEFAULT_LANG,
            markup: aiogram.types.InlineKeyboardMarkup = INLINE_EMPTY_KB,
            parse_mode: str = 'HTML') -> int:

        """
        :param user_id: integer, user id
        :param description: string, default = 'sorry, there was a problem, please try again later!'
        :param user_lang_code: lang code of user defaul - en
        :param markup: inline markup
        :param parse_mode: bot parsemode, default = HTML

        :returns: sended message id
        :raise Exception: if operation failed
        """

        if description is None:
            description = STATEMENTS_BY_LANG[user_lang_code].fatal_err

        else:
            description = BASE_STATEMENTS.exception_templ.format(description)

        sending_response = await self.bot.send_message(chat_id=user_id,
                                                       text=description,
                                                       parse_mode=parse_mode,
                                                       reply_markup=markup)

        return sending_response.message_id

    async def delete_message(
            self,
            user_id: int,
            message_id: list[int]) -> bool:

        """

        :param user_id: bot id of user
        :param message_id: id of the message you want to delete, integer or list of integers

        :returns: result of deleting
        :raise Exception: if operation failed

        """
        try:
            return await self.bot.delete_message(chat_id=user_id, message_id=message_id)

        except Exception as exception:
            raise exception
