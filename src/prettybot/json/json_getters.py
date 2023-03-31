import json
from src.prettybot.json.paths import paths


def get_setings_db() -> dict[str]:
    """
    function to get all settings of postgres database

    :returns: result of operation [string]
    """

    with open(paths.dictpaths['dbconfig'], 'r') as settings_file:
        return json.load(settings_file)


def get_token() -> dict[str]:
    """
    function to get bot token from file

    :returns: result of operation [string]
    """

    with open(paths.dictpaths['token'], 'r') as token_file:
        return token_file.readline()
