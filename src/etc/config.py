"""

global project variables

"""

from src.bot.bin.jsons import json_getters

TEMPLATES = json_getters.get_all_templates().object

LANG_STATEMENTS = json_getters.get_statements().object

LIMIT_REGISTRATION_STAGES = 6

STATEMENT_FOR_STAGE = {0: LANG_STATEMENTS['en']['select_lang'],
                       1: LANG_STATEMENTS['en']['q_age'],
                       2: LANG_STATEMENTS['en']['q_city'],
                       3: LANG_STATEMENTS['en']['q_sex'],
                       4: LANG_STATEMENTS['en']['q_desc'],
                       5: LANG_STATEMENTS['en']['q_photo']}

MAX_LEN_SAMPLING_CITIES = 15

MEDIUM_LEN_SAMPLING_CITIES = 4

TYPES_MAIN_MESSAGES = (0, 1, 2)

LANG_CODES = dict(en_lang_select='en',
                  ru_lang_select='ru')

STAGE_BY_PAYLOAD = dict(change_photo=5,
                        change_age=1,
                        change_city=2,
                        change_description=4)

DEFAULT_LANG = 'en'

MAX_DELAY_TIME_SECONDS = 20

DEFAULT_LOGGING_TYPE = 1
DEFAULT_LOGGING_STAGE = 1

STAGE_BLOCKED_TEXT_MESSAGES = (3, )

DEFAULT_DELAY = 2
