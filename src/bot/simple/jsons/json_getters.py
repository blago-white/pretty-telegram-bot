import json

from src.bot.simple import dataclass
from src.conf import paths


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
