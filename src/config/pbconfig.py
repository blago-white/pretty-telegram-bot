"""
global project variables
"""

from src.config.statements import en, ru, general
from src.prettybot.bot.db import sqltemplates

TEMPLATES = sqltemplates.templates

STATEMENTS_BY_LANG = {'en': en,
                      'ru': ru}

BASE_STATEMENTS = general
#  constants

MAX_LEN_SAMPLING_CITIES = 15

MEDIUM_LEN_SAMPLING_CITIES = 4

PROFILE_MESSAGE_TYPE = 0

QUESTION_MESSAGE_TYPE = 1

START_MESSAGE_TYPE = 2

TYPES_MAIN_MESSAGES = (PROFILE_MESSAGE_TYPE, QUESTION_MESSAGE_TYPE, START_MESSAGE_TYPE)

"""
0 - profile
1 - question message
2 - first message
"""

LANG_CODES = dict(en_lang_select='en',
                  ru_lang_select='ru')

QUESTION_STATEMENT_BY_CALLBACK_PAYLOAD_FINDING = {
    'change_age': {
        'ru': STATEMENTS_BY_LANG['ru'].q_age_range,
        'en': STATEMENTS_BY_LANG['en'].q_age_range
    },

    'change_city': {
        'ru': STATEMENTS_BY_LANG['ru'].q_new_city,
        'en': STATEMENTS_BY_LANG['en'].q_new_city
    },

    'change_sex': {
        'ru': STATEMENTS_BY_LANG['ru'].q_find_sex,
        'en': STATEMENTS_BY_LANG['en'].q_find_sex
    },
}

QUESTION_STATEMENT_BY_CALLBACK_PAYLOAD = {
    'change_photo': {
        'ru': STATEMENTS_BY_LANG['ru'].q_new_photo,
        'en': STATEMENTS_BY_LANG['en'].q_new_photo
    },

    'change_age': {
        'ru': STATEMENTS_BY_LANG['ru'].q_new_age,
        'en': STATEMENTS_BY_LANG['en'].q_new_age
    },

    'change_city': {
        'ru': STATEMENTS_BY_LANG['ru'].q_new_city,
        'en': STATEMENTS_BY_LANG['en'].q_new_city
    },

    'change_sex': {
        'ru': STATEMENTS_BY_LANG['ru'].q_sex,
        'en': STATEMENTS_BY_LANG['en'].q_sex
    },

    'change_description': {
        'ru': STATEMENTS_BY_LANG['ru'].q_new_desc,
        'en': STATEMENTS_BY_LANG['en'].q_new_desc
    }
}

DEFAULT_LANG = 'en'

MAX_DELAY_TIME_SECONDS = 20

DEFAULT_DELAY = 2

LONG_DELAY = 10

MEDIUM_DELAY = 5

LOWER_AGE_LIMIT = 10
UPPER_AGE_LIMIT = 99

MAX_LEN_DESCRIPTION = 350
