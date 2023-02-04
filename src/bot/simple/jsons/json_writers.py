import json

from src.bot.simple import dataclass, decorators
from src.conf import paths


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
    ...
    # with open(paths.dictpaths['tables'], 'w') as f:
    #     json.dump({"data": {"tables": ("users", "states", "users_info", "photos", "main_messages"),
    #                         "user_data_tables": ("users", "states", "users_info", "photos"),
    #                         "other_tables": ("main_messages",)}}, f)

