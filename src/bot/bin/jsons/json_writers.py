import json

from src.bot.module import decorators
from src.bot.bin import dataclass
from src.etc import paths


@decorators.trying()
def write_debug_mode(mode: bool) -> dataclass.ResultOperation:
    """

    :param mode: if true on next initializing database will happen drop all data from _db_scripts

    :returns: Result of operation

    """

    with open(paths.dictpaths['debug'], 'w') as file:
        file.write(str(mode))

    return dataclass.ResultOperation()


@decorators.trying()
def write_settings_db(**params: dict[str]) -> dataclass.ResultOperation:
    """

    function to set some settings for postgres database

    :returns: result of operation [string]

    """

    present_settings = get_setings_db().object
    for param_key in present_settings:
        if present_settings[param_key] != params[param_key]:
            present_settings[param_key] = params[param_key]

    with open(paths.dictpaths['dbconfig'], 'w') as settings_file:
        json.dump(present_settings, settings_file)

    return dataclass.ResultOperation(object=result)


@decorators.trying()
def write_condition(cond: bool) -> dataclass.ResultOperation:
    """

    set restarting _db_scripts mode

    :returns: result of operation

    """

    with open(paths.dictpaths['restore'], 'w') as file:
        json.dump({'restart': cond}, file)

    return dataclass.ResultOperation()


if __name__ == '__main__':
    pass
    # with open(paths.dictpaths['tables'], 'w') as f:
    #     json.dump({"data": {"tables": ("users", "states", "info_users", "photos", "main_messages"),
    #                         "user_data_tables": ("users", "states", "info_users", "photos"),
    #                         "other_tables": ("main_messages",)}}, f)

    with open(paths.dictpaths['templates'], 'w') as f:
        json.dump({1: "SELECT logging, logging_type, logging_stage FROM states WHERE telegram_id = {}",
                   3: "UPDATE states SET logging=False, logging_type=0, logging_stage=0 WHERE telegram_id={};",
                   4: "UPDATE states SET logging=True, logging_type={}, logging_stage={} WHERE telegram_id={};",
                   5: "INSERT INTO photos VALUES ({}, '{}');",
                   6: "UPDATE photos SET photo_id='{}' WHERE telegram_id={}",
                   7: "INSERT INTO users VALUES ({}, '{}', '{}', '{}', '{}', 'en');",
                   8: "INSERT INTO states VALUES ({}, {}, {}, {});",
                   9: "INSERT INTO info_users VALUES ({});",
                   10: "UPDATE info_users SET age={} WHERE telegram_id={};",
                   11: "UPDATE info_users SET city='{}' WHERE telegram_id={};",
                   12: "UPDATE info_users SET sex={} WHERE telegram_id={};",
                   13: "UPDATE info_users SET description='{}' WHERE telegram_id={};",
                   14: "INSERT INTO main_messages VALUES ({}, {}, {})",
                   15: "DELETE FROM main_messages WHERE telegram_id={} AND message_type={}",
                   16: "SELECT message_id FROM main_messages WHERE telegram_id={} AND message_type={}",
                   17: "SELECT * FROM {};",
                   19: "SELECT * FROM {} WHERE telegram_id = {};",
                   20: "DELETE FROM {} WHERE telegram_id = {};",
                   21: "UPDATE users SET language='{}' WHERE telegram_id={};",
                   }, f)

    with open(paths.dictpaths['statements_en'], 'w') as en_statements_file:
        json.dump(obj=dict(en=dict(welcome='\u270B hello, <b>{}</b>, i am - pretty bot, my creator - @VictorMerinov',
                                   welcome_back=u'<b>welcome back \u2764</b>',
                                   entry_registration='first you need to create your resume, <b>enter you age</b>',
                                   continue_warn='continue registration please:\n{}',
                                   acc_send_warn='your account did not sending try later',
                                   start_warn='send command /start to _bot please',
                                   help='if you find a bug, please tell me - @VictorMerinov and /restart the bot',
                                   change_lang_good='language succesfully changed to <b>English</b>',
                                   invalid_t_age='not correct value of age (10 - 99)',
                                   invalid_v_age='age must be integer (11, 12, ..., 99)',
                                   invalid_citi='enter a larger city please',
                                   invalid_l_desc="maximum lenhgt - 350 literals (you give '<b>{}</b> symbols)",
                                   invalid_t_photo='send only photo please',
                                   q_city='wich <b>city</b> wour from?',
                                   q_sex='what your <b>sex</b>?',
                                   q_desc='tell me a little <b>about you</b>',
                                   q_photo=u'\u2728last one, send me your future profile photo',
                                   q_age='how <b>old</b> are you?',
                                   btn_change=u'\u270Fchange info',
                                   btn_creator='🤙creator',
                                   btn_del_acc=u'\u2728find people',
                                   btn_en_lang='en🇬🇧',
                                   btn_ru_lang='ru🇷🇺',
                                   btn_back='📛back',
                                   btn_change_photo=u'\u270F photo',
                                   btn_change_age=u'\u270F age',
                                   btn_change_city=u'\u270F city',
                                   btn_change_description=u'\u270F description',
                                   fatal_err='sorry, there was a problem, please try again later!',
                                   city_sep=', ',
                                   select_lang='<b>select you language</b>',
                                   q_new_photo='send new frofile photo',
                                   q_new_age='enter new age',
                                   q_new_city='enter new city',
                                   q_new_desc='enter new description',
                                   profile_templ='{name}, {age} {declination}, {city}\n<i>{desc}</i>',
                                   man='i\'m man',
                                   woman='i\'m woman',
                                   overflow='...',
                                   exception_templ=u'🙃 {}'
                                   )),

                  fp=en_statements_file
                  )


