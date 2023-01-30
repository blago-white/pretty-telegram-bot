import json

from src.bot.module import decorators
from src.bot.bin import dataclass
from src.etc import paths


def get_setings_db() -> dataclass.ResultOperation:
    """

    function to get all settings of postgres database

    :returns: result of operation [string]

    """

    with open(paths.dictpaths['dbconfig'], 'r') as settings_file:
        result = json.load(settings_file)

    return dataclass.ResultOperation(object=result)


def get_token() -> dataclass.ResultOperation:
    """

    function to get telegram token from file

    :returns: result of operation [string]

    """

    with open(paths.dictpaths['token'], 'r') as token_file:
        result = token_file.readline()

    return dataclass.ResultOperation(object=result)


def get_all_templates() -> dataclass.ResultOperation:
    """

    get all templates to _db_scripts from a file

    :returns: result of operation [list of string templates]

    """

    path = paths.dictpaths['templates']

    with open(path, 'r') as file:
        data = json.load(file)

    return dataclass.ResultOperation(object=data)


def get_condition(field: str) -> dataclass.ResultOperation:
    """

    get restarting _db_scripts status

    :returns: result of operation

    """

    with open(paths.dictpaths['restore'], 'r') as file:
        data = json.load(file)

    return dataclass.ResultOperation(object=data[field])


def get_tables():
    with open(paths.dictpaths['tables'], 'r') as file:
        data = json.load(file)

    return dataclass.ResultOperation(object=data)


def get_statements():
    with open(paths.dictpaths['statements_en']) as statements_file:
        data = json.load(statements_file)

    return dataclass.ResultOperation(object=data)
