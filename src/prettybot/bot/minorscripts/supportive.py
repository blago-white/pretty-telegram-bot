import re
from typing import Union
import asyncio

from src.config.recording_stages import *
from src.prettybot.bot.callback.callback_keyboards import *


# 1
def get_age_declination(age: int) -> str:
    return 'год' if age % 10 == 1 else 'года' if age % 10 == 1 or 1 < age % 10 < 5 else 'лет'


# 3
def convert_sex_type(obj: Union[bool, str]) -> Union[bool, str]:
    if type(obj) is bool:
        return 'man' if obj else 'woman'

    return True if obj == 'man' else False


# 3
def search_cities_by_coincidence(string_idx: int, city: str, cities: dict[str], length_border: int) -> list:
    """
    :rtype: list
    """

    compressed_cities_list = [correct_city.capitalize()
                              for correct_city in cities
                              if correct_city[:string_idx]
                              == city[:string_idx]]

    if len(compressed_cities_list) <= length_border:
        return [cities[correct_city] for correct_city in cities if correct_city[:string_idx] == city[:string_idx]]

    return compressed_cities_list


# 3
def get_similar_cities(city: str, cities: dict) -> list:
    for string_idx in range(1, len(city) + 1):
        result_list = search_cities_by_coincidence(string_idx=string_idx,
                                                   city=city,
                                                   cities=cities,
                                                   length_border=MEDIUM_LEN_SAMPLING_CITIES)

        if not result_list:
            return result_list if string_idx == 1 else previous_cities

        previous_cities = result_list

    return result_list


# 1
def check_numbers_in_string(string: str) -> bool:
    return re.search(r'\d+', string)


# 2
def unpack_playload(payload_string: str) -> dict:
    return dict(type_request=payload_string.split('%')[0],
                type_requested_operation=payload_string.split('%')[1])


def generate_drop_down_cities_list(cities_list: list) -> str:
    if len(cities_list) > MAX_LEN_SAMPLING_CITIES:
        cities_list[MAX_LEN_SAMPLING_CITIES] += BASE_STATEMENTS.overflow
        cities_list = cities_list[:MAX_LEN_SAMPLING_CITIES + 1]

    return BASE_STATEMENTS.city_sep.join(cities_list)


# 3
def increase_stage_recording(stage_recording: str) -> str:
    return STAGES_RECORDING[STAGES_RECORDING.index(stage_recording) + 1
    if stage_recording != LAST_REGISTRATION_STAGE else STAGES_RECORDING.index(stage_recording)]


# 2
def get_inline_keyboard_by_stage(recordstage: str, recordtype: str) -> dict:
    if recordtype == TYPE_RECORDING[0] and recordstage in STAGES_RECORDING[1:3]:
        return INLINE_SEX_KB

    elif recordtype == TYPE_RECORDING[2] and recordstage == STAGES_RECORDING[2]:
        return INLINE_SEX_KB

    return INLINE_EMPTY_KB


# 1
def correct_text_to_db(text: str) -> str:
    return "'{}'".format(text.replace("'", "''").replace("/", ""))


# 3

def convert_dict_to_tuple(dict_: dict[str]) -> tuple[Union[str, tuple[str]]]:
    result = tuple(zip(dict_.keys(), dict_.values()))
    return result if len(result) > 1 else result[0]
