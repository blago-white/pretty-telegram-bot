import re
from typing import Union
import asyncio

from src.prettybot.dataclass import dataclass
from src.conf.pbconfig import MAX_DELAY_TIME_SECONDS, MEDIUM_LEN_SAMPLING_CITIES
from src.conf.recording_stages import *
from src.prettybot.callback.callback_keyboards import *


def get_age_declination(age: int) -> str:
    return 'год' if age % 10 == 1 else 'года' if age % 10 == 1 or 1 < age % 10 < 5 else 'лет'


def convert_sex_type(obj: Union[bool, str]) -> Union[bool, str]:
    if type(obj) is bool:
        return 'man' if obj else 'woman'

    return True if obj == 'man' else False


def search_cities_by_coincidence(string_idx: int, city: str, cities: dict[str], length_border: int) -> list:
    """
    :rtype: list
    """

    print(cities)
    compressed_cities_list = [correct_city.capitalize()
                              for correct_city in cities
                              if correct_city[:string_idx]
                              == city[:string_idx]]

    if len(compressed_cities_list) <= length_border:
        return [cities[correct_city] for correct_city in cities if correct_city[:string_idx] == city[:string_idx]]

    return compressed_cities_list


async def start_delay(delay: int) -> None:
    """
    :param delay: delay in seconds

    start the async delay
    """

    if 0 < int(delay) < MAX_DELAY_TIME_SECONDS:
        await asyncio.sleep(delay=int(delay))


def get_similar_cities(city: str, cities: dict) -> list:
    for string_idx in range(1, len(city) + 1):
        result_list = search_cities_by_coincidence(
            string_idx=string_idx,
            city=city,
            cities=cities,
            length_border=MEDIUM_LEN_SAMPLING_CITIES)

        if not result_list:
            return result_list if string_idx == 1 else previous_cities

        previous_cities = result_list

    return result_list


def check_numbers_in_string(string: str) -> bool:
    return re.search(r'\d+', string)


def unpack_playload(payload_string: str) -> dict:
    return dict(type_request=payload_string.split('%')[0],
                type_requested_operation=payload_string.split('%')[1])


def get_inline_keyboard_by_stage(stage: int) -> dict:
    return INLINE_SEX_KB if stage == STAGES_RECORDING[2] else INLINE_EMPTY_KB


def generate_drop_down_cities_list(cities_list: list) -> str:
    if len(cities_list) > MAX_LEN_SAMPLING_CITIES:
        cities_list[MAX_LEN_SAMPLING_CITIES] += BASE_STATEMENTS.overflow
        cities_list = cities_list[:MAX_LEN_SAMPLING_CITIES + 1]

    return BASE_STATEMENTS.city_sep.join(cities_list)


def increase_stage_recording(stage_recording: str) -> str:
    return STAGES_RECORDING[STAGES_RECORDING.index(stage_recording) + 1]
