from typing import Union

from src.prettybot.dataclass import dataclass
from src.prettybot.bot.minorscripts import supportive
from src.config.recording_stages import TYPE_RECORDING
from src.config.dbconfig import AMOUNT_CITIES

from src.config.pbconfig import *

__all__ = ['handle_message']


def handle_message(user_lang_code: str, record_stage: str, **kwargs) -> Union[dataclass.ResultOperation, str]:
    """
    kwargs values ---
    1. message text / file id {file id in handle photo}
    3. record_type / cities {handle age, handle city}
    4. record_stage

    :param record_stage: stage of recording
    :param user_lang_code: user language for statement

    :returns: your statement
    """
    try:
        text_handler = HANDLE_SCRIPT_BY_RECORDING_STAGE[record_stage]
        return text_handler(user_lang_code=user_lang_code, **kwargs)

    except KeyError:
        return


def _handle_age(user_lang_code: str, **kwargs) -> Union[str, dataclass.ResultOperation]:
    record_type = kwargs.get('record_type')
    message_text = kwargs.get('message_text')

    if record_type in TYPE_RECORDING[:2]:
        try:
            if not LOWER_AGE_LIMIT <= int(message_text) <= UPPER_AGE_LIMIT:
                return dataclass.ResultOperation(status=False, object=STATEMENTS_BY_LANG[user_lang_code].invalid_t_age)

            return dataclass.ResultOperation(status=True, object=STATEMENTS_BY_LANG[user_lang_code].q_city)

        except:
            return dataclass.ResultOperation(status=False,
                                             object=STATEMENTS_BY_LANG[user_lang_code].invalid_v_age)

    elif record_type == TYPE_RECORDING[2]:
        if supportive.check_numbers_in_string(string=message_text) is not None:
            numbers = [i for i in message_text if i.isdigit()]

            if len(numbers) < 4:
                return dataclass.ResultOperation(status=False,
                                                 object=STATEMENTS_BY_LANG[user_lang_code].invalid_v_range_age)

            return dataclass.ResultOperation(status=True)

        else:
            return dataclass.ResultOperation(status=False,
                                             object=STATEMENTS_BY_LANG[user_lang_code].invalid_t_range_age)


def _handle_city(user_lang_code: str, **kwargs):
    cities = kwargs.get('cities')
    message_text = kwargs.get('message_text')

    if str.lower(str(message_text)) not in cities:
        simular_cities = supportive.get_similar_cities(city=str.lower(message_text), cities=cities)
        if simular_cities:
            return dataclass.ResultOperation(status=False,
                                             object=supportive.generate_drop_down_cities_list(
                                                 cities_list=simular_cities)
                                             )

        return dataclass.ResultOperation(status=False, object=STATEMENTS_BY_LANG[user_lang_code].invalid_citi)

    return dataclass.ResultOperation(status=True, object=STATEMENTS_BY_LANG[user_lang_code].q_sex)


def _handle_sex(user_lang_code: str, **kwargs):
    record_type = kwargs.get('record_type')

    if record_type == TYPE_RECORDING[0]:
        return dataclass.ResultOperation(status=False, object=STATEMENTS_BY_LANG[user_lang_code].q_sex)

    elif record_type == TYPE_RECORDING[2]:
        return dataclass.ResultOperation(status=False, object=STATEMENTS_BY_LANG[user_lang_code].q_find_sex)


def _handle_description(user_lang_code: str, **kwargs):
    message_text = kwargs.get('message_text')

    if len(message_text) > MAX_LEN_DESCRIPTION:
        return dataclass.ResultOperation(status=False,
                                         object=STATEMENTS_BY_LANG[user_lang_code].invalid_l_desc.format(
                                             len(message_text)
                                         ))

    return dataclass.ResultOperation(status=True, object=STATEMENTS_BY_LANG[user_lang_code].q_photo)


def _handle_photo(user_lang_code: str, **_):
    return dataclass.ResultOperation(status=False,
                                     object=STATEMENTS_BY_LANG[user_lang_code].invalid_t_photo)


HANDLE_SCRIPT_BY_RECORDING_STAGE = {
    'age': _handle_age,
    'cty': _handle_city,
    'sex': _handle_sex,
    'dsc': _handle_description,
    'pht': _handle_photo,
}
