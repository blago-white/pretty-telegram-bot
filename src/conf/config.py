"""

global project variables

"""

from src.conf.docs.statements import en, ru, general
from src.conf.docs import sqltemplates

TEMPLATES = sqltemplates.templates

STATEMENTS_BY_LANG = {'en': en,
                      'ru': ru}

BASE_STATEMENTS = general
#  constants

LIMIT_REGISTRATION_STAGES = 6

STATEMENT_FOR_STAGE = {'en': {
    1: STATEMENTS_BY_LANG['en'].q_age,
    2: STATEMENTS_BY_LANG['en'].q_city,
    3: STATEMENTS_BY_LANG['en'].q_sex,
    4: STATEMENTS_BY_LANG['en'].q_desc,
    5: STATEMENTS_BY_LANG['en'].q_photo
},

    'ru': {
        1: STATEMENTS_BY_LANG['ru'].q_age,
        2: STATEMENTS_BY_LANG['ru'].q_city,
        3: STATEMENTS_BY_LANG['ru'].q_sex,
        4: STATEMENTS_BY_LANG['ru'].q_desc,
        5: STATEMENTS_BY_LANG['ru'].q_photo
    }}

MAX_LEN_SAMPLING_CITIES = 15

MEDIUM_LEN_SAMPLING_CITIES = 4

TYPES_MAIN_MESSAGES = (0, 1, 2)

"""
0 - profile
1 - question message
2 - first message
"""

LANG_CODES = dict(en_lang_select='en',
                  ru_lang_select='ru')

STAGE_BY_PAYLOAD = dict(change_photo=5,
                        change_age=1,
                        change_city=2,
                        change_description=4)

DEFAULT_LANG = 'en'

MAX_DELAY_TIME_SECONDS = 20

STAGE_BLOCKED_TEXT_MESSAGES = (3,)

DEFAULT_DELAY = 2

LONG_DELAY = 10

NAME_COLUMN_BY_LOGSTAGE = {
    1: 'age',
    2: 'city',
    3: 'sex',
    4: 'description'
}

WISHES_COLUMNS = (1, 2, 3)

LOWER_AGE_LIMIT = 10
UPPER_AGE_LIMIT = 99

MAX_LEN_DESCRIPTION = 350
