from src.config.pbconfig import *

LENGHT_TYPE_RECORDING_VAL = 3
LENGHT_STAGE_RECORDING_VAL = 3

TYPE_RECORDING = [
    'int',
    'acc',
    'fnd'
]

AGE_STAGE = 'age'

CITY_STAGE = 'cty'

SEX_STAGE = 'sex'

DESCRIPTION_STAGE = 'dsc'

PHOTO_STAGE = 'pht'

STAGES_RECORDING = [
    AGE_STAGE,
    CITY_STAGE,
    SEX_STAGE,
    DESCRIPTION_STAGE,
    PHOTO_STAGE
]

LAST_REGISTRATION_STAGE = STAGES_RECORDING[-1]

MAIN_REGISTRATION_TYPE = (TYPE_RECORDING[0])

STATEMENT_FOR_STAGE = dict(
    en=dict(
        age=STATEMENTS_BY_LANG['en'].q_age,
        cty=STATEMENTS_BY_LANG['en'].q_city,
        sex=STATEMENTS_BY_LANG['en'].q_sex,
        dsc=STATEMENTS_BY_LANG['en'].q_desc,
        pht=STATEMENTS_BY_LANG['en'].q_photo
    ),

    ru=dict(
        age=STATEMENTS_BY_LANG['ru'].q_age,
        cty=STATEMENTS_BY_LANG['ru'].q_city,
        sex=STATEMENTS_BY_LANG['ru'].q_sex,
        dsc=STATEMENTS_BY_LANG['ru'].q_desc,
        pht=STATEMENTS_BY_LANG['ru'].q_photo
    ))

STAGE_BY_PAYLOAD = dict(change_photo=STAGES_RECORDING[4],
                        change_age=STAGES_RECORDING[0],
                        change_sex=STAGES_RECORDING[2],
                        change_city=STAGES_RECORDING[1],
                        change_description=STAGES_RECORDING[3])

MAIN_RECORDING_TYPE = TYPE_RECORDING[0]

STAGE_BLOCKED_TEXT_MESSAGES = (SEX_STAGE,)

NAME_COLUMN_BY_LOGSTAGE = {
    STAGES_RECORDING[0]: AGE_STAGE,
    STAGES_RECORDING[1]: 'city',
    STAGES_RECORDING[2]: SEX_STAGE,
    STAGES_RECORDING[3]: 'description'
}

COLUMNS_WITH_WISHES = (AGE_STAGE + '_wish', 'city_wish', SEX_STAGE + '_wish')

NAME_WISH_COLUMN_BY_LOGSTAGE = {
    STAGES_RECORDING[0]: COLUMNS_WITH_WISHES[0],
    STAGES_RECORDING[1]: COLUMNS_WITH_WISHES[1],
    STAGES_RECORDING[2]: COLUMNS_WITH_WISHES[2],
}

SEARCH_PARAM_COLUMNS = (AGE_STAGE, CITY_STAGE, SEX_STAGE)
