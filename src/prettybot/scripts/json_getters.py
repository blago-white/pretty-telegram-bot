import json

from src.prettybot.dataclass import dataclass
from src.conf.paths import paths


def get_setings_db() -> dataclass.ResultOperation:
    """

    function to get all settings of postgres database

    :returns: result of operation [string]

    """

    with open(paths.dictpaths['dbconfig'], 'r') as settings_file:
        return dataclass.ResultOperation(object=json.load(settings_file))


def get_token() -> dataclass.ResultOperation:
    """

    function to get bot token from file

    :returns: result of operation [string]

    """

    with open(paths.dictpaths['token'], 'r') as token_file:
        return dataclass.ResultOperation(object=token_file.readline())
