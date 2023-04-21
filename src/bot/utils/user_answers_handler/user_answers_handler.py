import inspect
from typing import Union, Tuple

from . import _similar_cities_view

from src.bot.utils import lightscripts
from src.bot.config.recording_stages import TYPE_RECORDING

from ...config.pbconfig import *
from ...config.cities_config import *

__all__ = ['handle_message']


def handle_message(user_lang_code: str,
                   record_stage: str,
                   **kw) -> Tuple[bool, Union[str, Union[str, None]]]:
    """
    kwargs values ---
    1. message text / file id {file id in handle photo}
    3. record_type {handle age}
    4. record_stage

    :param record_stage: stage of recording
    :param user_lang_code: user language for statement

    :returns: your statement
    :except KeyError: if handler didn't get all the arguments
    """
    try:
        text_handler = _HANDLE_SCRIPT_BY_RECORDING_STAGE[record_stage]
        return text_handler(user_lang_code=user_lang_code, **kw)

    except KeyError:
        raise KeyError()


def _handle_age(user_lang_code: str, **kwargs) -> Union[Tuple[bool, Union[str, None]], KeyError]:
    record_type = kwargs.get('record_type')
    message_text = kwargs.get('message_text')

    if record_type in TYPE_RECORDING[:2]:
        try:
            if not LOWER_AGE_LIMIT <= int(message_text) <= UPPER_AGE_LIMIT:
                return False, STATEMENTS_BY_LANG[user_lang_code].invalid_t_age

            return True, STATEMENTS_BY_LANG[user_lang_code].q_city

        except:
            return False, STATEMENTS_BY_LANG[user_lang_code].invalid_v_age

    elif record_type == TYPE_RECORDING[2]:
        digits = lightscripts.get_digits_from_string(string=message_text)
        if digits is not None:
            if len(digits) < 4:
                return False, STATEMENTS_BY_LANG[user_lang_code].invalid_v_range_age

            return True,

        else:
            return False, STATEMENTS_BY_LANG[user_lang_code].invalid_t_range_age


def _handle_city(user_lang_code: str, **kwargs) -> Union[Tuple[bool, str], KeyError]:
    message_text = kwargs.get('message_text')

    if str.lower(str(message_text)) not in BOT_SUPPORTED_CITIES_LISTING:
        similar_cities = _similar_cities_view.get_similar_cities_list(city=str.lower(message_text))
        if similar_cities:
            return False, similar_cities

        return False, STATEMENTS_BY_LANG[user_lang_code].invalid_citi
    return True, STATEMENTS_BY_LANG[user_lang_code].q_sex


def _handle_sex(user_lang_code: str, **kwargs) -> Union[Tuple[bool, str], KeyError]:
    record_type = kwargs.get('record_type')

    if record_type == TYPE_RECORDING[0]:
        return False, STATEMENTS_BY_LANG[user_lang_code].q_sex

    elif record_type == TYPE_RECORDING[2]:
        return False, STATEMENTS_BY_LANG[user_lang_code].q_find_sex


def _handle_description(user_lang_code: str, **kwargs) -> Union[Tuple[bool, str], KeyError]:
    message_text = kwargs.get('message_text')

    if len(message_text) > MAX_LEN_DESCRIPTION:
        return False, STATEMENTS_BY_LANG[user_lang_code].invalid_l_desc.format(len(message_text))

    return True, STATEMENTS_BY_LANG[user_lang_code].q_photo


def _handle_photo(user_lang_code: str, **_) -> Tuple[bool, str]:
    return False, STATEMENTS_BY_LANG[user_lang_code].invalid_t_photo


_HANDLE_SCRIPT_BY_RECORDING_STAGE = {
    'age': _handle_age,
    'cty': _handle_city,
    'sex': _handle_sex,
    'dsc': _handle_description,
    'pht': _handle_photo,
}
