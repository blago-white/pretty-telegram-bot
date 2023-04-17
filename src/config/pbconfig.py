from .statements import en, ru, general
from .cities_config import BOT_SUPPORTED_CITIES_LISTING

STATEMENTS_BY_LANG = {'en': en, 'ru': ru}

BASE_STATEMENTS = general

MAX_LEN_SAMPLING_CITIES = 15

MEDIUM_LEN_SAMPLING_CITIES = 4

ALLOWED_CHAT_TYPES = ('private', )

BOT_COMMANDS = {'start': ('start',),
                'help': ('help',),
                'restart': ('restart',),
                'lang': ('en', 'ru'),
                'end': ('end',)}

BOT_CONTENT_TYPES = {'photo': ('photo',),
                     'text': ('text',)}

LANG_CODES = dict(en_lang_select='en',
                  ru_lang_select='ru')

DEFAULT_AGE_RANGE_OFFSET = 5

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

CITY_NAME_ABBREVIATIONS = {'область': 'обл.',
                           'Республика': 'Респ.',
                           'автономный округ': 'a.о.',
                           'автономная область': 'a.обл.'}

CITI_LONG_VIEW = '<b>{}</b> [{}]'

DEFAULT_AGE_DECLINATION = 'лет'

AGE_DECLINATIONS = [DEFAULT_AGE_DECLINATION, 'год', 'года']

DEFAULT_LANG = 'en'

MAX_DELAY_TIME_SECONDS = 20

DEFAULT_DELAY = 2

LONG_DELAY = 10

MEDIUM_DELAY = 5

LOWER_AGE_LIMIT = 10

UPPER_AGE_LIMIT = 99

MAX_LEN_DESCRIPTION = 350
