from typing import Union

TEMPLATES = []


def set_templates(templates: dict):
    global TEMPLATES
    TEMPLATES = templates


def fill_sql_template(*args, number_temp: int) -> Union[str, Exception]:
    """
    :param args: areguments which will be inserted into the template
    :param number_temp: number of template (see the numbers in sqltemplates.py)
    :return: string - querry with your data or exception
    """

    global TEMPLATES

    if not number_temp:
        return IndexError('not correct number template')

    try:
        if TEMPLATES:
            return TEMPLATES[number_temp].format(*args)

    except IndexError:
        return IndexError('Not correct number of template of not full args')
