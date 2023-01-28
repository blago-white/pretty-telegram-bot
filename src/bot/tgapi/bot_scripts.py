import aiogram
from src.bot.bin import dataclass
from src.etc.config import MAX_LEN_SAMPLING_CITIES, LANG_STATEMENTS
from typing import Union


def generate_drop_down_cities_list(pylist: list):
    if len(pylist) > MAX_LEN_SAMPLING_CITIES:
        pylist[MAX_LEN_SAMPLING_CITIES] += LANG_STATEMENTS['en']['overflow']
        pylist = pylist[:MAX_LEN_SAMPLING_CITIES + 1]

    return LANG_STATEMENTS['en']['city_sep'].join(pylist)


def get_statement_by_stage(
        db_scripts,
        message: aiogram.types.Message,
        logstage: int
) -> dataclass.ResultOperation:
    """

    :returns ResultOperation()*


    *** status = True if message is good, obj = statement[string]

    """

    if logstage == 1:

        try:
            age = int(message.text)

            if not 10 < age < 99:
                return dataclass.ResultOperation(status=False, obj=LANG_STATEMENTS['en']['invalid_t_age'])

            return dataclass.ResultOperation(status=True, obj=LANG_STATEMENTS['en']['q_city'])

        except:
            return dataclass.ResultOperation(status=False, obj=LANG_STATEMENTS['en']['invalid_v_age'])

    elif logstage == 2:
        if str.lower(str(message.text)) not in db_scripts.all_cities:

            simular_cities = db_scripts.get_similar_cities(city=str.lower(message.text)).object

            if simular_cities:
                return dataclass.ResultOperation(status=False, obj=generate_drop_down_cities_list(simular_cities))

            return dataclass.ResultOperation(status=False, obj=LANG_STATEMENTS['en']['invalid_citi'])

        return dataclass.ResultOperation(status=True, obj=LANG_STATEMENTS['en']['q_sex'])

    elif logstage == 3:
        if message.text in ('/man', '/woman'):
            return dataclass.ResultOperation(status=True, obj=LANG_STATEMENTS['en']['q_desc'])

        return dataclass.ResultOperation(status=False, obj=LANG_STATEMENTS['en']['invalid_t_sex'])

    elif logstage == 4:

        if len(message.text) > 350:
            return dataclass.ResultOperation(status=False,
                                             obj=LANG_STATEMENTS['en']['invalid_l_desc'].format(
                                                 len(message.text)
                                             ))

        return dataclass.ResultOperation(status=True, obj=LANG_STATEMENTS['en']['q_photo'])

        # 'last one, send me your future profile photo!'

    elif logstage == 5:
        if message['photo']:
            return dataclass.ResultOperation(status=True)

        # 'send only photo please'
        return dataclass.ResultOperation(status=False, obj=LANG_STATEMENTS['en']['invalid_t_photo'])

    raise ValueError(logstage)


def get_profile_body(
        name: str,
        age: int,
        city: str,
        desc: str) -> Union[dataclass.ResultOperation, str]:
    """

    :param name:
    :param age:
    :param city:
    :param desc:

    :retuens: Dataclasses.ResultOperation object

    """

    declination = 'лет'

    if age % 10 == 1:
        declination = 'год'

    elif 1 < age % 10 < 5:
        declination = 'года'

    account_text = LANG_STATEMENTS['en']['profile_templ'].format(name=name,
                                                                 age=age,
                                                                 declination=declination,
                                                                 city=city.capitalize(),
                                                                 desc=desc
                                                                 )

    return dataclass.ResultOperation(obj=account_text)
