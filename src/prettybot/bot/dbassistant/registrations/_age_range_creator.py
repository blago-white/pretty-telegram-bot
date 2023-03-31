import psycopg2.extras

from src.config.pbconfig import *
from src.config.recording_stages import *


def _create_age_range_limits(message_payload: str) -> dict[int]:
    start_range, stop_range = (int(message_payload) - DEFAULT_AGE_RANGE_OFFSET,
                               int(message_payload) + DEFAULT_AGE_RANGE_OFFSET)

    return dict(start=max(start_range, LOWER_AGE_LIMIT), stop=min(stop_range, UPPER_AGE_LIMIT))


def _retrieve_age_range_limits(message_payload: str) -> dict[int]:
    age_digits = [int(i) for i in message_payload if i.isdigit()][:4]
    age_range = age_digits[0] * 10 + age_digits[1], age_digits[2] * 10 + age_digits[3]

    return dict(start=min(age_range), stop=max(age_range))


def get_age_range_limits(message_payload: str, recording_type: str) -> dict[int]:
    if recording_type in TYPE_RECORDING[:2]:
        return _create_age_range_limits(message_payload=message_payload)

    elif recording_type == TYPE_RECORDING[2]:
        return _retrieve_age_range_limits(message_payload=message_payload)


def get_age_range_for_db(start_range: int, stop_range: int) -> str:
    return "'{}'::int4range".format(psycopg2.extras.NumericRange(lower=int(start_range),
                                                                 upper=int(stop_range),
                                                                 bounds='[]'))
